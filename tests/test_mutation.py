import pytest
from unittest.mock import patch, MagicMock

from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.evaluation_result import EvaluationResult
from stem_agent.schemas.prompt_section import PromptSection
from stem_agent.services.evolution.mutation import MutationEngine


@pytest.fixture
def current_config():
    return AgentConfig(
        task_class="generic",
        prompt_sections={
            "role": PromptSection(content="You are a generic assistant."),
            "strategy": PromptSection(content="Original strategy content."),
            "quality_constraints": PromptSection(content="Original quality content."),
            "output_format": PromptSection(content="Plain text.")
        },
        created_from="baseline"
    )


@pytest.fixture
def low_insight_evaluation():
    return EvaluationResult(coverage=4.0, grounding=4.0, insight=2.0, feedback="Insight was weak.")


@pytest.fixture
def low_grounding_evaluation():
    return EvaluationResult(coverage=4.0, grounding=2.0, insight=4.0, feedback="Grounding was weak.")


@patch("stem_agent.services.evolution.mutation.ChatOpenAI")
def test_mutation_targets_strategy_when_insight_is_low(mock_openai, current_config, low_insight_evaluation):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = MagicMock(content="Improved strategy content.")
    mock_openai.return_value = mock_instance

    engine = MutationEngine(low_insight_evaluation)
    new_config = engine.mutate(current_config)

    assert new_config.prompt_sections["strategy"].content == "Improved strategy content."
    assert new_config.prompt_sections["strategy"].version == 2
    assert new_config.prompt_sections["quality_constraints"].content == "Original quality content."


@patch("stem_agent.services.evolution.mutation.ChatOpenAI")
def test_mutation_targets_quality_constraints_when_grounding_is_low(mock_openai, current_config, low_grounding_evaluation):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = MagicMock(content="Improved quality content.")
    mock_openai.return_value = mock_instance

    engine = MutationEngine(low_grounding_evaluation)
    new_config = engine.mutate(current_config)

    assert new_config.prompt_sections["quality_constraints"].content == "Improved quality content."
    assert new_config.prompt_sections["strategy"].content == "Original strategy content."


@patch("stem_agent.services.evolution.mutation.ChatOpenAI")
def test_mutation_increments_config_version(mock_openai, current_config, low_insight_evaluation):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = MagicMock(content="Improved content.")
    mock_openai.return_value = mock_instance

    engine = MutationEngine(low_insight_evaluation)
    new_config = engine.mutate(current_config)

    assert new_config.version == current_config.version + 1


@patch("stem_agent.services.evolution.mutation.ChatOpenAI")
def test_mutation_sets_mutation_reason(mock_openai, current_config, low_insight_evaluation):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = MagicMock(content="Improved content.")
    mock_openai.return_value = mock_instance

    engine = MutationEngine(low_insight_evaluation)
    new_config = engine.mutate(current_config)

    assert new_config.prompt_sections["strategy"].mutation_reason is not None
    assert "insight" in new_config.prompt_sections["strategy"].mutation_reason.lower()


@patch("stem_agent.services.evolution.mutation.ChatOpenAI")
def test_mutation_preserves_unmutated_sections(mock_openai, current_config, low_insight_evaluation):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = MagicMock(content="Improved content.")
    mock_openai.return_value = mock_instance

    engine = MutationEngine(low_insight_evaluation)
    new_config = engine.mutate(current_config)

    assert new_config.prompt_sections["role"].content == current_config.prompt_sections["role"].content
    assert new_config.prompt_sections["output_format"].content == current_config.prompt_sections["output_format"].content


@patch("stem_agent.services.evolution.mutation.ChatOpenAI")
def test_mutation_raises_on_empty_llm_output(mock_openai, current_config, low_insight_evaluation):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = MagicMock(content="   ")
    mock_openai.return_value = mock_instance

    engine = MutationEngine(low_insight_evaluation)
    with pytest.raises(ValueError):
        engine.mutate(current_config)


@patch("stem_agent.services.evolution.mutation.ChatOpenAI")
def test_mutation_propagates_llm_exception(mock_openai, current_config, low_insight_evaluation):
    mock_instance = MagicMock()
    mock_instance.invoke.side_effect = Exception("LLM down")
    mock_openai.return_value = mock_instance

    engine = MutationEngine(low_insight_evaluation)
    with pytest.raises(Exception, match="LLM down"):
        engine.mutate(current_config)