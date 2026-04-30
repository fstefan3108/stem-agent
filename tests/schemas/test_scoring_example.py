import pytest
from pydantic import ValidationError

from stem_agent.schemas.scoring_example import ScoringExample


@pytest.fixture
def valid_scoring_example_data():
    return {
        "task_input": "Research AI agent frameworks.",
        "example_output": "LangChain, AutoGen, and CrewAI are popular frameworks.",
        "coverage": 3.0,
        "grounding": 3.5,
        "insight": 2.5,
        "coverage_rationale": "Covers main frameworks but lacks depth.",
        "grounding_rationale": "Names real frameworks with minimal detail.",
        "insight_rationale": "Lists frameworks without comparison or tradeoffs."
    }


def test_valid_scoring_example(valid_scoring_example_data):
    example = ScoringExample(**valid_scoring_example_data)
    assert example.task_input == "Research AI agent frameworks."
    assert example.coverage == 3.0
    assert example.grounding == 3.5
    assert example.insight == 2.5


def test_invalid_task_input_empty(valid_scoring_example_data):
    valid_scoring_example_data["task_input"] = ""
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_task_input_whitespace(valid_scoring_example_data):
    valid_scoring_example_data["task_input"] = "   "
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_example_output_empty(valid_scoring_example_data):
    valid_scoring_example_data["example_output"] = ""
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_coverage_below_one(valid_scoring_example_data):
    valid_scoring_example_data["coverage"] = 0.5
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_coverage_above_five(valid_scoring_example_data):
    valid_scoring_example_data["coverage"] = 6.0
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_grounding_below_one(valid_scoring_example_data):
    valid_scoring_example_data["grounding"] = 0.0
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_grounding_above_five(valid_scoring_example_data):
    valid_scoring_example_data["grounding"] = 5.5
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_insight_below_one(valid_scoring_example_data):
    valid_scoring_example_data["insight"] = 0.5
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_insight_above_five(valid_scoring_example_data):
    valid_scoring_example_data["insight"] = 10.0
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_coverage_rationale_empty(valid_scoring_example_data):
    valid_scoring_example_data["coverage_rationale"] = ""
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_grounding_rationale_whitespace(valid_scoring_example_data):
    valid_scoring_example_data["grounding_rationale"] = "   "
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)


def test_invalid_insight_rationale_empty(valid_scoring_example_data):
    valid_scoring_example_data["insight_rationale"] = ""
    with pytest.raises(ValidationError):
        ScoringExample(**valid_scoring_example_data)