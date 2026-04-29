from stem_agent.agents.stem_agent import StemAgent
from stem_agent.core.logger import logger
from stem_agent.services.initialization.agent_config_factory import generate_default_agent_config


def main():
    default_config = generate_default_agent_config()
    stem_agent = StemAgent(agent_config=default_config)

    user_query = input("Ask the stem agent anything. It can adapt to your task's complexity over lifecycles.\n\nEnter message: ").strip()
    if not user_query:
        print("Please enter a task.")
        return

    try:
        answer = stem_agent.run(user_query)
        logger.info(f"Stem Agent: {answer.strip()}")
    except Exception as e:
        logger.error(f"Execution failed: {e}")

if __name__ == "__main__":
    main()