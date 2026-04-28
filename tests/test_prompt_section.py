import pytest
from pydantic import ValidationError

from stem_agent.schemas.prompt_section import PromptSection


def test_valid_prompt_section():
    prompt_section = PromptSection(
        name="role",
        content="You are an agent",
        version=3,
        mutable=True,
        mutation_reason="Improved aspect coverage"
    )
    assert prompt_section.name == "role"
    assert prompt_section.content == "You are an agent"
    assert prompt_section.version == 3
    assert prompt_section.mutable is True
    assert prompt_section.mutation_reason == "Improved aspect coverage"

def test_invalid_prompt_section_name():
    with pytest.raises(ValidationError):
        PromptSection(
            name="",
            content="You are an agent",
            version=1,
            mutable=True,
            mutation_reason=None
        )

def test_invalid_prompt_section_content():
    with pytest.raises(ValidationError):
        PromptSection(
            name="role",
            content="",
            version=1,
            mutable=True,
            mutation_reason=None
        )

def test_invalid_prompt_section_version():
    with pytest.raises(ValidationError):
        PromptSection(
            name="role",
            content="You are an agent",
            version=0,
            mutable=True,
            mutation_reason=None
        )

def test_invalid_prompt_non_mutable_section_version():
    with pytest.raises(ValidationError):
        PromptSection(
            name="role",
            content="You are an agent",
            version=3,
            mutable=False,
            mutation_reason=None
        )

def test_invalid_prompt_non_mutable_section_has_mutation_reason():
    with pytest.raises(ValidationError):
        PromptSection(
            name="role",
            content="You are an agent",
            version=1,
            mutable=False,
            mutation_reason="Improved aspect coverage"
        )

def test_invalid_prompt_mutable_section_without_mutation_reason():
    with pytest.raises(ValidationError):
        PromptSection(
            name="role",
            content="You are an agent",
            version=3,
            mutable=True,
            mutation_reason=None
        )