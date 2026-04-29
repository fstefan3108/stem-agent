from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.prompt_section import PromptSection


def generate_default_agent_config() -> AgentConfig:
    """Returns the default generic baseline AgentConfig for the stem agent."""
    return AgentConfig(
        task_class="generic",
        available_tools=[],
        prompt_sections={
            "role": PromptSection(content="You are a general-purpose assistant."),
            "strategy": PromptSection(content="Read the user's request and respond as best you can."),
            "quality_constraints": PromptSection(content="Provide a response that addresses the user's request."),
            "output_format": PromptSection(content="Respond in plain text.")
        },
        version=1,
        stages=[],
        created_from="generic_baseline"
    )