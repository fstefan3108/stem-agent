import pytest
from unittest.mock import patch, MagicMock

from stem_agent.schemas.evaluation_result import EvaluationResult
from stem_agent.schemas.scoring_example import ScoringExample
from stem_agent.services.evaluation.evaluator import EvaluationService


@pytest.fixture
def scoring_examples():
    return [
        ScoringExample(
            task_input="Research X.",
            example_output="X is a thing.",
            coverage=2.0,
            grounding=2.0,
            insight=2.0,
            coverage_rationale="Shallow.",
            grounding_rationale="Vague.",
            insight_rationale="No analysis."
        )
    ]


@patch("stem_agent.services.evaluation.evaluator.ChatOpenAI")
def test_evaluate_returns_evaluation_result(mock_openai, scoring_examples):
    mock_instance = MagicMock()
    mock_instance.with_structured_output.return_value = mock_instance
    mock_instance.invoke.return_value = EvaluationResult(
        coverage=3.0, grounding=3.0, insight=3.0, feedback="Mocked feedback."
    )
    mock_openai.return_value = mock_instance

    service = EvaluationService(scoring_examples)
    result = service.evaluate("Research the topic.", "Some response.")
    assert isinstance(result, EvaluationResult)
    assert result.coverage == 3.0


@patch("stem_agent.services.evaluation.evaluator.ChatOpenAI")
def test_evaluate_raises_on_empty_user_task(mock_openai, scoring_examples):
    mock_openai.return_value = MagicMock()
    service = EvaluationService(scoring_examples)
    with pytest.raises(ValueError):
        service.evaluate("", "Some response.")


@patch("stem_agent.services.evaluation.evaluator.ChatOpenAI")
def test_evaluate_raises_on_whitespace_user_task(mock_openai, scoring_examples):
    mock_openai.return_value = MagicMock()
    service = EvaluationService(scoring_examples)
    with pytest.raises(ValueError):
        service.evaluate("   ", "Some response.")


@patch("stem_agent.services.evaluation.evaluator.ChatOpenAI")
def test_evaluate_raises_on_empty_stem_agent_answer(mock_openai, scoring_examples):
    mock_openai.return_value = MagicMock()
    service = EvaluationService(scoring_examples)
    with pytest.raises(ValueError):
        service.evaluate("Research the topic.", "")


@patch("stem_agent.services.evaluation.evaluator.ChatOpenAI")
def test_evaluate_reraises_on_llm_failure(mock_openai, scoring_examples):
    mock_instance = MagicMock()
    mock_instance.with_structured_output.return_value = mock_instance
    mock_instance.invoke.side_effect = Exception("LLM failed")
    mock_openai.return_value = mock_instance

    service = EvaluationService(scoring_examples)
    with pytest.raises(Exception, match="LLM failed"):
        service.evaluate("Research the topic.", "Some response.")