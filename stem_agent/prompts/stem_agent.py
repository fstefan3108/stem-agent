from datetime import datetime, UTC
from textwrap import dedent

from stem_agent.schemas.agent_config import AgentConfig


def build_stem_agent_prompt(user_query: str, agent_config: AgentConfig) -> str:
    user_query = user_query.strip()
    prompt = dedent(f"""
CURRENT DATE AND TIME: {datetime.now(UTC)}

ROLE
{agent_config.prompt_sections["role"].content}

STRATEGY
{agent_config.prompt_sections["strategy"].content}

QUALITY CONSTRAINTS
{agent_config.prompt_sections["quality_constraints"].content}

OUTPUT FORMAT
{agent_config.prompt_sections["output_format"].content}

TASK
{user_query}
        """).strip()
    return prompt