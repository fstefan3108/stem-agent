from datetime import datetime, UTC
from textwrap import dedent
from langchain_openai import ChatOpenAI

from stem_agent.core.logger import logger
from stem_agent.core.settings import settings
from stem_agent.schemas.agent_config import AgentConfig


class StemAgent:
    """A configurable LLM agent whose behavior is driven entirely by an AgentConfig."""
    def __init__(self, agent_config: AgentConfig):
        self.config = agent_config

        self.llm = ChatOpenAI(
            model=settings.STEM_AGENT_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )

    def run(self, user_query: str) -> str:
        if not user_query.strip():
            raise ValueError("User query cannot be empty or whitespace.")

        try:
            prompt = self._build_prompt(user_query)
            return self.llm.invoke(prompt).content

        except Exception as e:
            logger.error(f"Failed to run agent: {e}")
            raise

    def _build_prompt(self, user_query: str) -> str:
        user_query = user_query.strip()
        prompt = dedent(f"""
CURRENT DATE AND TIME: {datetime.now(UTC)}

ROLE
{self.config.prompt_sections["role"].content}

STRATEGY
{self.config.prompt_sections["strategy"].content}

QUALITY CONSTRAINTS
{self.config.prompt_sections["quality_constraints"].content}

OUTPUT FORMAT
{self.config.prompt_sections["output_format"].content}

TASK
{user_query}
        """).strip()
        return prompt
