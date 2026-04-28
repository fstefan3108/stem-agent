import pytest
from pydantic import ValidationError

from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.prompt_section import PromptSection


@pytest.fixture
def valid_prompt_sections():
    return {
        "role": PromptSection(content="You are a generic stem agent."),
        "strategy": PromptSection(content="Break the task down before answering."),
        "quality_constraints": PromptSection(content="Cover all required aspects."),
        "output_format": PromptSection(content="Use clear sections.")
    }

def test_valid_agent_config(valid_prompt_sections):
    agent_config = AgentConfig(
        task_class="deep researcher",
        available_tools=["deep_research", "web_search"],
        prompt_sections=valid_prompt_sections,
        max_steps=9,
        version=2,
        stages=["stage1", "stage2"],
        created_from="initialization phase"
    )

    assert agent_config.task_class == "deep researcher"
    assert agent_config.available_tools == ["deep_research", "web_search"]
    assert agent_config.prompt_sections == valid_prompt_sections
    assert agent_config.max_steps == 9
    assert agent_config.version == 2
    assert agent_config.stages == ["stage1", "stage2"]
    assert agent_config.created_from == "initialization phase"

def test_invalid_agent_config_task_class_empty_string(valid_prompt_sections):
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class="",
            available_tools=["deep_research", "web_search"],
            prompt_sections=valid_prompt_sections,
            max_steps=9,
            version=2,
            stages=["stage1", "stage2"],
            created_from="initialization phase"
        )

def test_invalid_agent_config_task_class_white_space(valid_prompt_sections):
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class=" ",
            available_tools=["deep_research", "web_search"],
            prompt_sections=valid_prompt_sections,
            max_steps=9,
            version=2,
            stages=["stage1", "stage2"],
            created_from="initialization phase"
        )

def test_invalid_agent_config_max_steps_greater_than_ten(valid_prompt_sections):
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class="deep researcher",
            available_tools=["deep_research", "web_search"],
            prompt_sections=valid_prompt_sections,
            max_steps=12,
            version=2,
            stages=["stage1", "stage2"],
            created_from="initialization phase"
        )

def test_invalid_agent_config_task_class_max_steps_less_than_one(valid_prompt_sections):
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class="deep researcher",
            available_tools=["deep_research", "web_search"],
            prompt_sections=valid_prompt_sections,
            max_steps=0,
            version=2,
            stages=["stage1", "stage2"],
            created_from="initialization phase"
        )

def test_invalid_agent_config_version(valid_prompt_sections):
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class="deep researcher",
            available_tools=["deep_research", "web_search"],
            prompt_sections=valid_prompt_sections,
            max_steps=9,
            version=0,
            stages=["stage1", "stage2"],
            created_from="initialization phase"
        )

def test_invalid_agent_config_created_from_empty_string(valid_prompt_sections):
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class="deep researcher",
            available_tools=["deep_research", "web_search"],
            prompt_sections=valid_prompt_sections,
            max_steps = 9,
            version = 1,
            stages = ["stage1", "stage2"],
            created_from = ""
        )

def test_invalid_agent_config_created_from_white_space(valid_prompt_sections):
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class="deep researcher",
            available_tools=["deep_research", "web_search"],
            prompt_sections=valid_prompt_sections,
            max_steps = 9,
            version = 1,
            stages = ["stage1", "stage2"],
            created_from = " "
        )

def test_invalid_agent_config_missing_section_keys():
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class="deep researcher",
            available_tools=["deep_research", "web_search"],
            prompt_sections={
                "role": PromptSection(content="Role."),
                "strategy": PromptSection(content="Strategy."),
                "quality_constraints": PromptSection(content="Quality_constraints."),
            },
            max_steps=9,
            version=1,
            stages=["stage1", "stage2"],
            created_from="initialization phase"
        )

def test_invalid_agent_config_extra_section_keys():
    with pytest.raises(ValidationError):
        AgentConfig(
            task_class="deep researcher",
            available_tools=["deep_research", "web_search"],
            prompt_sections={
                "role": PromptSection(content="Role."),
                "strategy": PromptSection(content="Strategy."),
                "quality_constraints": PromptSection(content="Quality_constraints."),
                "output_format": PromptSection(content="Use clear sections."),
                "extra_information": PromptSection(content="Search the internet.")
            },
            max_steps=9,
            version=1,
            stages=["stage1", "stage2"],
            created_from="initialization phase"
        )