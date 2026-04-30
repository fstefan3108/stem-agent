from unittest.mock import patch, MagicMock
import pytest

from stem_agent.agents.stem_agent import StemAgent
from stem_agent.prompts.stem_agent import build_stem_agent_prompt
from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.prompt_section import PromptSection


@pytest.fixture
def valid_agent_config():
    return AgentConfig(
        task_class="generic",
        prompt_sections={
            "role": PromptSection(content="You are a generic assistant."),
            "strategy": PromptSection(content="Answer directly."),
            "quality_constraints": PromptSection(content="Be accurate."),
            "output_format": PromptSection(content="Plain text.")
        },
        created_from="generic_baseline"
    )

@patch("stem_agent.agents.stem_agent.ChatOpenAI")
def test_valid_run_returns_answer(mock_openai, valid_agent_config):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value = MagicMock(content="mocked answer")
    mock_openai.return_value = mock_instance

    agent = StemAgent(valid_agent_config)
    result = agent.run("Research the latest AI framework.")
    assert result == "mocked answer"

@patch("stem_agent.agents.stem_agent.ChatOpenAI")
def test_invalid_run_empty_query(mock_openai, valid_agent_config):
    mock_openai.return_value = MagicMock()
    agent = StemAgent(valid_agent_config)
    with pytest.raises(ValueError):
        agent.run("")

@patch("stem_agent.agents.stem_agent.ChatOpenAI")
def test_invalid_run_whitespace(mock_openai, valid_agent_config):
    mock_openai.return_value = MagicMock()
    agent = StemAgent(valid_agent_config)
    with pytest.raises(ValueError):
        agent.run(" ")

@patch("stem_agent.agents.stem_agent.ChatOpenAI")
def test_build_prompt_contains_all_sections(mock_openai, valid_agent_config):
    mock_openai.return_value = MagicMock()
    prompt = build_stem_agent_prompt("Research AI frameworks.", valid_agent_config)

    assert "You are a generic assistant." in prompt
    assert "Answer directly." in prompt
    assert "Be accurate." in prompt
    assert "Plain text." in prompt
    assert "Research AI frameworks." in prompt