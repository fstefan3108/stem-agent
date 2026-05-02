import traceback

from stem_agent.core.logger import logger
from stem_agent.services.evolution.engine import EvolutionEngine
from stem_agent.services.initialization.agent_config_factory import generate_default_agent_config


def main():
    user_query = input("Enter a deep research task:\n\n").strip()
    if not user_query:
        print("Please enter a task.")
        return

    initial_config = generate_default_agent_config()
    evolution_engine = EvolutionEngine(initial_config=initial_config, max_iterations=3)

    try:
        final_config = evolution_engine.run(user_query)

        logger.info("[EVOLUTION COMPLETE]")
        logger.info(f"Final config version: {final_config.version}")
        logger.info(f"Iterations recorded: {len(evolution_engine.history)}")
        logger.info(f"Accepted mutations: {sum(1 for r in evolution_engine.history if r.accepted)}")
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()