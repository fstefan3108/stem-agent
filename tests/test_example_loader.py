import json

import pytest
from pydantic import ValidationError

from stem_agent.schemas.task_example import TaskExample
from stem_agent.services.initialization.example_loader import load_task_examples


def test_valid_load_dataset(tmp_path):
    dataset = [
        {
            "task_input": "Research AI frameworks.",
            "example_output": "LangChain is a framework...",
            "quality_label": "good",
            "notes": ["Well structured", "Has tradeoffs"]
        }
    ]
    dataset_file = tmp_path / "dataset.json"
    dataset_file.write_text(json.dumps(dataset))

    result = load_task_examples(dataset_file)
    assert len(result) == 1
    assert isinstance(result[0], TaskExample)

def test_invalid_load_empty_dataset(tmp_path):
    dataset = []
    dataset_file = tmp_path / "dataset.json"
    dataset_file.write_text(json.dumps(dataset))

    with pytest.raises(ValueError):
        load_task_examples(dataset_file)

def test_invalid_load_dataset_not_found(tmp_path):
    non_existent = tmp_path / "does_not_exist.json"
    with pytest.raises(FileNotFoundError):
        load_task_examples(non_existent)

def test_invalid_load_dataset_schema(tmp_path):
    dataset = [{"task_input": ""}]
    dataset_file = tmp_path / "dataset.json"
    dataset_file.write_text(json.dumps(dataset))
    with pytest.raises(ValidationError):
        load_task_examples(dataset_file)

def test_invalid_load_dataset_root_not_list(tmp_path):
    dataset_file = tmp_path / "dataset.json"
    dataset_file.write_text(json.dumps({"task_input": "bad"}))
    with pytest.raises(ValueError):
        load_task_examples(dataset_file)