from langchain_openai import ChatOpenAI

from stem_agent.core.logger import logger
from stem_agent.core.settings import settings
from stem_agent.prompts.evaluator import build_evaluator_prompt
from stem_agent.schemas.evaluation_result import EvaluationResult
from stem_agent.schemas.scoring_example import ScoringExample


class EvaluationService:
    """LLM-driven evaluation service that scores stem agent responses against a fixed scoring rubric."""
    def __init__(self, scoring_examples: list[ScoringExample]):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.EVALUATOR_MODEL,
            temperature=0
        ).with_structured_output(EvaluationResult, method="function_calling")

        self.scoring_examples = scoring_examples

    def evaluate(self, user_task: str, stem_agent_answer: str) -> EvaluationResult:
        user_task = user_task.strip()
        stem_agent_answer = stem_agent_answer.strip()

        if not user_task:
            raise ValueError("No user task provided.")
        if not stem_agent_answer:
            raise ValueError("Stem Agent failed to provide answer.")

        prompt = build_evaluator_prompt(
            user_task=user_task,
            stem_agent_answer=stem_agent_answer,
            scoring_examples=self.scoring_examples
        )
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"[EVALUATOR] Error: Evaluation failed: {e}")
            raise