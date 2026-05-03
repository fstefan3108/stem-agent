from stem_agent.core.constants import REQUIRED_PROMPT_SECTION_KEYS
from stem_agent.services.initialization.agent_config_factory import generate_default_agent_config


def test_generate_default_agent_config():
    config = generate_default_agent_config()
    assert config.task_class == "generic"
    assert config.created_from == "generic_baseline"
    assert config.version == 1
    assert set(config.prompt_sections.keys()) == REQUIRED_PROMPT_SECTION_KEYS