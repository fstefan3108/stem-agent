import pytest
from pydantic import ValidationError

from stem_agent.schemas.evaluation_result import EvaluationResult


def test_valid_evaluation_result():
    evaluation_result = EvaluationResult(
        coverage=2,
        grounding=4,
        insight=5,
        feedback="The research went mostly well overall but more attention to coverage of user's requests."
    )

    assert evaluation_result.coverage == 2
    assert evaluation_result.grounding == 4
    assert evaluation_result.insight == 5
    assert evaluation_result.feedback == "The research went mostly well overall but more attention to coverage of user's requests."

def test_invalid_coverage_below_one():
    with pytest.raises(ValidationError):
        EvaluationResult(
            coverage=0,
            grounding=4,
            insight=5,
            feedback="The research went mostly well overall but more attention to coverage of user's requests."
        )

def test_invalid_coverage_above_five():
    with pytest.raises(ValidationError):
        EvaluationResult(
            coverage=6,
            grounding=4,
            insight=5,
            feedback="The research went mostly well overall but more attention to coverage of user's requests."
        )

def test_invalid_grounding_below_one():
    with pytest.raises(ValidationError):
        EvaluationResult(
            coverage=3,
            grounding=0,
            insight=5,
            feedback="The research went mostly well overall but more attention to coverage of user's requests."
        )

def test_invalid_grounding_above_five():
    with pytest.raises(ValidationError):
        EvaluationResult(
            coverage=3,
            grounding=6,
            insight=5,
            feedback="The research went mostly well overall but more attention to coverage of user's requests."
        )

def test_invalid_insight_below_one():
    with pytest.raises(ValidationError):
        EvaluationResult(
            coverage=3,
            grounding=4,
            insight=0,
            feedback="The research went mostly well overall but more attention to coverage of user's requests."
        )

def test_invalid_insight_above_five():
    with pytest.raises(ValidationError):
        EvaluationResult(
            coverage=3,
            grounding=4,
            insight=6,
            feedback="The research went mostly well overall but more attention to coverage of user's requests."
        )

def test_invalid_feedback_empty_string():
    with pytest.raises(ValidationError):
        EvaluationResult(
            coverage=3,
            grounding=4,
            insight=5,
            feedback=""
        )

def test_invalid_feedback_whitespace():
    with pytest.raises(ValidationError):
        EvaluationResult(
            coverage=3,
            grounding=4,
            insight=5,
            feedback=" "
        )

def test_score_calculation():
    evaluation_result = EvaluationResult(
        coverage=3,
        grounding=4,
        insight=5,
        feedback="The research went mostly well overall but more attention to coverage of user's requests."
    )
    assert evaluation_result.total_score == 4.0