from stem_agent.agents.stem_agent import StemAgent
from stem_agent.core.logger import logger
from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.enums import PromptSectionKey
from stem_agent.schemas.evaluation_result import EvaluationResult
from stem_agent.schemas.evolution_record import EvolutionRecord
from stem_agent.services.evaluation.evaluator import EvaluationService
from stem_agent.services.evolution.mutation import MutationEngine
from stem_agent.services.initialization.example_loader import load_scoring_examples


class EvolutionEngine:
    """Orchestrates the evolution loop: mutate, evaluate, compare, accept or reject."""
    def __init__(self, initial_config: AgentConfig, max_iterations: int = 10, improvement_threshold: float = 0.5):
        self.current_config = initial_config
        self.max_iterations = max_iterations
        self.threshold = improvement_threshold

        self.evaluator = EvaluationService(load_scoring_examples())
        self.mutation_engine = MutationEngine()
        self.history: list[EvolutionRecord] = []

    def run(self, user_task: str) -> AgentConfig:
        current_eval = self._evaluate_config(self.current_config, user_task)

        consecutive_rejections = 0

        for iteration in range(1, self.max_iterations + 1):
            try:
                candidate_config = self.mutation_engine.mutate(
                    current_config=self.current_config,
                    evaluation_result=current_eval
                )

                mutated_section = self._find_mutated_section(self.current_config, candidate_config)
                if mutated_section is None:
                    logger.warning(f"[ITERATION {iteration}] no-op mutation, skipping.")
                    # Note to self: No-op doesn't count as a rejection — mutation engine simply produced nothing
                    continue

                candidate_eval = self._evaluate_config(candidate_config, user_task)

                accepted = candidate_eval.total_score >= current_eval.total_score + self.threshold
                self._log_iteration(
                    iteration=iteration,
                    current_eval=current_eval,
                    candidate_eval=candidate_eval,
                    candidate_config=candidate_config,
                    mutated_section=mutated_section,
                    accepted=accepted
                )

                if accepted:
                    consecutive_rejections = 0
                    self.current_config = candidate_config
                    current_eval = candidate_eval
                else:
                    consecutive_rejections += 1
                    if consecutive_rejections >= 3:
                        logger.info(f"[STOP] 3 consecutive rejections, ending evolution.")
                        break

            except Exception as e:
                logger.error(f"[ITERATION {iteration}] failed: {e}")
                continue

        return self.current_config

    def _log_iteration(
            self,
            iteration: int,
            current_eval: EvaluationResult,
            candidate_eval: EvaluationResult,
            candidate_config: AgentConfig,
            mutated_section: PromptSectionKey,
            accepted: bool
    ) -> EvolutionRecord:
        evolution_record = EvolutionRecord(
            iteration=iteration,
            current_config_version=self.current_config.version,
            candidate_config_version=candidate_config.version,
            current_score=current_eval.total_score,
            candidate_score=candidate_eval.total_score,
            accepted=accepted,
            mutation_target=mutated_section,
            mutation_reason=candidate_config.prompt_sections[mutated_section].mutation_reason,
            evaluator_feedback=candidate_eval.feedback
        )
        self.history.append(evolution_record)
        return evolution_record

    def _evaluate_config(self, config: AgentConfig, user_task: str) -> EvaluationResult:
        stem_agent = StemAgent(config)
        answer = stem_agent.run(user_task)
        logger.info(f"[STEM AGENT v{config.version}]: {answer}...")
        evaluation = self.evaluator.evaluate(user_task=user_task, stem_agent_answer=answer)
        logger.info(f"[EVALUATION v{config.version}] coverage: {evaluation.coverage}\n grounding: {evaluation.grounding} \ninsight: {evaluation.insight}")
        return evaluation

    @staticmethod
    def _find_mutated_section(current: AgentConfig, candidate: AgentConfig) -> PromptSectionKey | None:
        for key in current.prompt_sections:
            if current.prompt_sections[key].content != candidate.prompt_sections[key].content:
                return PromptSectionKey(key)
        return None