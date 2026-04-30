from langchain_openai import ChatOpenAI

from stem_agent.core.constants import LOW_METRIC_TO_SECTION
from stem_agent.core.logger import logger
from stem_agent.core.settings import settings
from stem_agent.prompts.prompt_mutator import build_mutator_prompt
from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.evaluation_result import EvaluationResult
from stem_agent.schemas.prompt_section import PromptSection


class MutationEngine:
    """Generates a single-section mutation of an AgentConfig based on the lowest evaluation metric."""
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.PROMPT_GENERATOR_MODEL,
            temperature=0
        )

    def mutate(self, current_config: AgentConfig, evaluation_result: EvaluationResult) -> AgentConfig:
        weak_metric, targeted_section = self._find_weak_metric_and_section(evaluation_result)

        mutated_section_content = self._rewrite_section_content(
            current_config=current_config,
            targeted_section=targeted_section,
            weak_metric=weak_metric
        )

        if not mutated_section_content.strip():
            raise ValueError("No new section content was provided.")

        mutated_prompt_section = PromptSection(
            content=mutated_section_content,
            version=current_config.prompt_sections[targeted_section].version + 1,
            mutable=True,
            mutation_reason = f"Targeted low {weak_metric} score."
        )

        new_sections = dict(current_config.prompt_sections)
        new_sections[targeted_section] = mutated_prompt_section

        return AgentConfig(
            task_class=current_config.task_class,
            available_tools=current_config.available_tools,
            prompt_sections=new_sections,
            version=current_config.version + 1,
            created_from=f"mutation_v{current_config.version + 1}"
        )

    def _rewrite_section_content(
            self,
            current_config: AgentConfig,
            targeted_section: str,
            weak_metric: str,
            evaluation_result: EvaluationResult
    ) -> str:

        prompt = build_mutator_prompt(
            current_section_content=current_config.prompt_sections[targeted_section].content,
            target_section_name=targeted_section,
            weak_metric=weak_metric,
            evaluator_feedback=evaluation_result.feedback,
        )
        try:
            return self.llm.invoke(prompt).content
        except Exception as e:
            logger.error(f"[MUTATION ENGINE] Failed to run mutation engine: {e}")
            raise

    @staticmethod
    def _find_weak_metric_and_section(evaluation_result: EvaluationResult) -> tuple[str, str]:
        metrics = {
            "coverage": evaluation_result.coverage,
            "grounding": evaluation_result.grounding,
            "insight": evaluation_result.insight,
        }
        lowest_metric = min(metrics, key=metrics.get)
        target_section = LOW_METRIC_TO_SECTION[lowest_metric]
        return lowest_metric, target_section