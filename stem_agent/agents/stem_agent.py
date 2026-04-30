from langchain_openai import ChatOpenAI

from stem_agent.core.logger import logger
from stem_agent.core.settings import settings
from stem_agent.prompts.stem_agent import build_stem_agent_prompt
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
            prompt = build_stem_agent_prompt(user_query=user_query, agent_config=self.config)
            return self.llm.invoke(prompt).content

        except Exception as e:
            logger.error(f"Failed to run agent: {e}")
            raise