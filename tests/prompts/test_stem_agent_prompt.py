from stem_agent.prompts.stem_agent import build_stem_agent_prompt
from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.prompt_section import PromptSection


def test_stem_agent_prompt_contains_all_sections_and_query():
    config = AgentConfig(
        task_class="generic",
        prompt_sections={
            "role": PromptSection(content="Role content here."),
            "strategy": PromptSection(content="Strategy content here."),
            "quality_constraints": PromptSection(content="Quality content here."),
            "output_format": PromptSection(content="Output content here.")
        },
        created_from="baseline"
    )
    prompt = build_stem_agent_prompt("Research AI frameworks.", config)

    assert "Role content here." in prompt
    assert "Strategy content here." in prompt
    assert "Quality content here." in prompt
    assert "Output content here." in prompt
    assert "Research AI frameworks." in prompt