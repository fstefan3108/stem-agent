import pytest
from unittest.mock import patch, MagicMock

from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.evaluation_result import EvaluationResult
from stem_agent.schemas.prompt_section import PromptSection
from stem_agent.services.evolution.engine import EvolutionEngine


@pytest.fixture
def initial_config():
    return AgentConfig(
        task_class="generic",
        prompt_sections={
            "role": PromptSection(content="You are an assistant."),
            "strategy": PromptSection(content="Original strategy."),
            "quality_constraints": PromptSection(content="Original quality."),
            "output_format": PromptSection(content="Plain text."),
        },
        created_from="baseline",
    )


@pytest.fixture
def make_evaluation():
    def _make(coverage=4.0, grounding=4.0, insight=4.0, feedback="Test feedback."):
        return EvaluationResult(
            coverage=coverage, grounding=grounding, insight=insight, feedback=feedback
        )
    return _make


def _build_candidate(initial_config: AgentConfig, new_strategy_content: str, version: int = 2) -> AgentConfig:
    new_sections = dict(initial_config.prompt_sections)
    new_sections["strategy"] = PromptSection(
        content=new_strategy_content,
        version=version,
        mutable=True,
        mutation_reason="Test mutation.",
    )
    return AgentConfig(
        task_class=initial_config.task_class,
        available_tools=initial_config.available_tools,
        prompt_sections=new_sections,
        version=version,
        created_from="mutation",
    )


@patch("stem_agent.services.evolution.engine.MutationEngine")
@patch("stem_agent.services.evolution.engine.EvaluationService")
@patch("stem_agent.services.evolution.engine.StemAgent")
@patch("stem_agent.services.evolution.engine.load_scoring_examples")
def test_run_accepts_improving_mutation(
    mock_loader, mock_agent_cls, mock_eval_cls, mock_mut_cls, initial_config, make_evaluation
):
    mock_loader.return_value = []

    mock_agent = MagicMock()
    mock_agent.run.return_value = "Some answer."
    mock_agent_cls.return_value = mock_agent

    mock_eval = MagicMock()
    mock_eval.evaluate.side_effect = [
        make_evaluation(coverage=2.0, grounding=2.0, insight=2.0),
        make_evaluation(coverage=4.0, grounding=4.0, insight=4.0),
    ]
    mock_eval_cls.return_value = mock_eval

    candidate_config = _build_candidate(initial_config, "Mutated strategy.")

    mock_mut = MagicMock()
    mock_mut.mutate.return_value = candidate_config
    mock_mut_cls.return_value = mock_mut

    engine = EvolutionEngine(initial_config=initial_config, max_iterations=1)
    final = engine.run("research task")

    assert final.version == 2
    assert len(engine.history) == 1
    assert engine.history[0].accepted is True


@patch("stem_agent.services.evolution.engine.MutationEngine")
@patch("stem_agent.services.evolution.engine.EvaluationService")
@patch("stem_agent.services.evolution.engine.StemAgent")
@patch("stem_agent.services.evolution.engine.load_scoring_examples")
def test_run_rejects_non_improving_mutation(
    mock_loader, mock_agent_cls, mock_eval_cls, mock_mut_cls, initial_config, make_evaluation
):
    mock_loader.return_value = []

    mock_agent = MagicMock()
    mock_agent.run.return_value = "Some answer."
    mock_agent_cls.return_value = mock_agent

    mock_eval = MagicMock()
    mock_eval.evaluate.side_effect = [
        make_evaluation(coverage=4.0, grounding=4.0, insight=4.0),
        make_evaluation(coverage=4.1, grounding=4.0, insight=4.0),
    ]
    mock_eval_cls.return_value = mock_eval

    candidate_config = _build_candidate(initial_config, "Slightly different.")

    mock_mut = MagicMock()
    mock_mut.mutate.return_value = candidate_config
    mock_mut_cls.return_value = mock_mut

    engine = EvolutionEngine(initial_config=initial_config, max_iterations=1)
    final = engine.run("research task")

    assert final.version == 1
    assert len(engine.history) == 1
    assert engine.history[0].accepted is False


@patch("stem_agent.services.evolution.engine.MutationEngine")
@patch("stem_agent.services.evolution.engine.EvaluationService")
@patch("stem_agent.services.evolution.engine.StemAgent")
@patch("stem_agent.services.evolution.engine.load_scoring_examples")
def test_run_skips_no_op_mutation(
    mock_loader, mock_agent_cls, mock_eval_cls, mock_mut_cls, initial_config, make_evaluation
):
    mock_loader.return_value = []

    mock_agent = MagicMock()
    mock_agent.run.return_value = "Some answer."
    mock_agent_cls.return_value = mock_agent

    mock_eval = MagicMock()
    mock_eval.evaluate.return_value = make_evaluation()
    mock_eval_cls.return_value = mock_eval

    no_op_sections = dict(initial_config.prompt_sections)
    no_op_config = AgentConfig(
        task_class=initial_config.task_class,
        available_tools=initial_config.available_tools,
        prompt_sections=no_op_sections,
        version=2,
        created_from="mutation",
    )
    mock_mut = MagicMock()
    mock_mut.mutate.return_value = no_op_config
    mock_mut_cls.return_value = mock_mut

    engine = EvolutionEngine(initial_config=initial_config, max_iterations=2)
    final = engine.run("research task")

    assert final.version == 1
    assert len(engine.history) == 0


@patch("stem_agent.services.evolution.engine.MutationEngine")
@patch("stem_agent.services.evolution.engine.EvaluationService")
@patch("stem_agent.services.evolution.engine.StemAgent")
@patch("stem_agent.services.evolution.engine.load_scoring_examples")
def test_run_stops_at_max_iterations(
    mock_loader, mock_agent_cls, mock_eval_cls, mock_mut_cls, initial_config, make_evaluation
):
    mock_loader.return_value = []

    mock_agent = MagicMock()
    mock_agent.run.return_value = "Some answer."
    mock_agent_cls.return_value = mock_agent

    mock_eval = MagicMock()
    mock_eval.evaluate.return_value = make_evaluation(coverage=2.0, grounding=2.0, insight=2.0)
    mock_eval_cls.return_value = mock_eval

    counter = {"calls": 0}

    def make_candidate(**kwargs):
        counter["calls"] += 1
        return _build_candidate(initial_config, f"Mutation {counter['calls']}.", version=1 + counter["calls"])

    mock_mut = MagicMock()
    mock_mut.mutate.side_effect = make_candidate
    mock_mut_cls.return_value = mock_mut

    engine = EvolutionEngine(initial_config=initial_config, max_iterations=3)
    engine.run("research task")

    assert mock_mut.mutate.call_count == 3


def test_find_mutated_section_detects_change(initial_config):
    candidate = _build_candidate(initial_config, "Different content.")
    result = EvolutionEngine._find_mutated_section(initial_config, candidate)
    assert result.value == "strategy"


def test_find_mutated_section_returns_none_on_no_change(initial_config):
    candidate = AgentConfig(
        task_class=initial_config.task_class,
        available_tools=initial_config.available_tools,
        prompt_sections=dict(initial_config.prompt_sections),
        version=initial_config.version,
        created_from=initial_config.created_from,
    )
    result = EvolutionEngine._find_mutated_section(initial_config, candidate)
    assert result is None