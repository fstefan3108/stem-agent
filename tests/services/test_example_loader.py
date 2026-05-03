import json
import pytest
from pydantic import ValidationError

from stem_agent.schemas.scoring_example import ScoringExample
from stem_agent.services.initialization.example_loader import load_scoring_examples


def test_valid_load_dataset(tmp_path):
    dataset = [
        {
            "task_input": "Research AI frameworks.",
            "example_output": "LangChain is a framework with a large ecosystem.",
            "coverage": 3.0,
            "grounding": 2.5,
            "insight": 2.0,
            "coverage_rationale": "Names the framework but lacks scope.",
            "grounding_rationale": "Mentions ecosystem but no specifics.",
            "insight_rationale": "No comparison or recommendation."
        }
    ]
    dataset_file = tmp_path / "scoring_examples.json"
    dataset_file.write_text(json.dumps(dataset))

    result = load_scoring_examples(dataset_file)
    assert len(result) == 1
    assert isinstance(result[0], ScoringExample)


def test_invalid_load_empty_dataset(tmp_path):
    dataset = []
    dataset_file = tmp_path / "scoring_examples.json"
    dataset_file.write_text(json.dumps(dataset))

    with pytest.raises(ValueError):
        load_scoring_examples(dataset_file)


def test_invalid_load_dataset_not_found(tmp_path):
    non_existent = tmp_path / "does_not_exist.json"
    with pytest.raises(FileNotFoundError):
        load_scoring_examples(non_existent)


def test_invalid_load_dataset_schema(tmp_path):
    dataset = [{"task_input": ""}]
    dataset_file = tmp_path / "scoring_examples.json"
    dataset_file.write_text(json.dumps(dataset))
    with pytest.raises(ValidationError):
        load_scoring_examples(dataset_file)


def test_invalid_load_dataset_root_not_list(tmp_path):
    dataset_file = tmp_path / "scoring_examples.json"
    dataset_file.write_text(json.dumps({"task_input": "bad"}))
    with pytest.raises(ValueError):
        load_scoring_examples(dataset_file)