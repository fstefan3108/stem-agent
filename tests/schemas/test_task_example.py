import pytest
from pydantic import ValidationError

from stem_agent.schemas.task_example import TaskExample


def test_valid_task_example():
    task_example = TaskExample(
        task_input="Perform a deep research on the latest langchain technologies.",
        example_output="Langchain is an agentic framework for developing AI agents...",
        quality_label="good",
        notes=[
            "Coverage was good, but utilization of sources here was...",
            "Generate a better research plan before using the tool..."
        ]
    )

    assert task_example.task_input == "Perform a deep research on the latest langchain technologies."
    assert task_example.example_output == "Langchain is an agentic framework for developing AI agents..."
    assert task_example.quality_label == "good"
    assert task_example.notes == [
        "Coverage was good, but utilization of sources here was...",
        "Generate a better research plan before using the tool..."
    ]

def test_invalid_task_input_empty_string():
    with pytest.raises(ValidationError):
        TaskExample(
            task_input="",
            example_output="Langchain is an agentic framework for developing AI agents...",
            quality_label="good",
            notes=[
                "Coverage was good, but utilization of sources here was...",
                "Generate a better research plan before using the tool..."
            ]
        )

def test_invalid_task_input_whitespace():
    with pytest.raises(ValidationError):
        TaskExample(
            task_input=" ",
            example_output="Langchain is an agentic framework for developing AI agents...",
            quality_label="good",
            notes=[
                "Coverage was good, but utilization of sources here was...",
                "Generate a better research plan before using the tool..."
            ]
        )

def test_invalid_example_output_empty_string():
    with pytest.raises(ValidationError):
        TaskExample(
            task_input="Perform a deep research on the latest langchain technologies.",
            example_output="",
            quality_label="good",
            notes=[
                "Coverage was good, but utilization of sources here was...",
                "Generate a better research plan before using the tool..."
            ]
        )

def test_invalid_example_output_whitespace():
    with pytest.raises(ValidationError):
        TaskExample(
            task_input="Perform a deep research on the latest langchain technologies.",
            example_output=" ",
            quality_label="good",
            notes=[
                "Coverage was good, but utilization of sources here was...",
                "Generate a better research plan before using the tool..."
            ]
        )

def test_invalid_quality_label():
    with pytest.raises(ValidationError):
        TaskExample(
            task_input="Perform a deep research on the latest langchain technologies.",
            example_output="Langchain is an agentic framework for developing AI agents...",
            quality_label="unknown",
            notes=[
                "Coverage was good, but utilization of sources here was...",
                "Generate a better research plan before using the tool..."
            ]
        )

def test_invalid_notes_empty_note():
    with pytest.raises(ValidationError):
        TaskExample(
            task_input="Perform a deep research on the latest langchain technologies.",
            example_output="Langchain is an agentic framework for developing AI agents...",
            quality_label="good",
            notes=[
                "Coverage was good, but utilization of sources here was...",
                ""
            ]
        )

def test_invalid_notes_whitespace_note():
    with pytest.raises(ValidationError):
        TaskExample(
            task_input="Perform a deep research on the latest langchain technologies.",
            example_output="Langchain is an agentic framework for developing AI agents...",
            quality_label="good",
            notes=[
                "Coverage was good, but utilization of sources here was...",
                " "
            ]
        )