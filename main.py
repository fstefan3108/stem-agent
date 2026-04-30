import traceback

from stem_agent.agents.stem_agent import StemAgent
from stem_agent.core.logger import logger
from stem_agent.services.evaluation.evaluator import EvaluationService
from stem_agent.services.evolution.mutation import MutationEngine
from stem_agent.services.initialization.agent_config_factory import generate_default_agent_config
from stem_agent.services.initialization.example_loader import load_scoring_examples


def main():
    default_config = generate_default_agent_config()
    stem_agent = StemAgent(agent_config=default_config)

    user_query = input("Ask the stem agent anything. It can adapt to your task's complexity over lifecycles.\n\nEnter message: ").strip()
    if not user_query:
        print("Please enter a task.")
        return

    try:
        answer = stem_agent.run(user_query)
        logger.info(f"[STEM AGENT]: {answer.strip()}")

        evaluator = EvaluationService(load_scoring_examples())
        evaluation = evaluator.evaluate(user_task=user_query, stem_agent_answer=answer)
        logger.info(f"[EVALUATOR]: {evaluation}")

        mutation_engine = MutationEngine()
        mutated_config = mutation_engine.mutate(current_config=default_config, evaluation_result=evaluation)
        logger.info(f"[MUTATION ENGINE]: {mutated_config}")
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()