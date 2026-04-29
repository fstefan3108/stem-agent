from stem_agent.agents.stem_agent import StemAgent
from stem_agent.core.logger import logger
from stem_agent.services.initialization.agent_config_factory import generate_default_agent_config
from stem_agent.services.initialization.config_refinement_engine import AgentConfigRefinementEngine
from stem_agent.services.initialization.example_loader import load_task_examples


def main():
    default_config = generate_default_agent_config()
    agent_config_refinement_engine = AgentConfigRefinementEngine(
        current_config=default_config,
        task_examples=load_task_examples(),
    )

    new_agent_config = agent_config_refinement_engine.generate_refined_agent_config()
    logger.info(f"[CONFIG REFINEMENT ENGINE]: {new_agent_config}")

    stem_agent = StemAgent(agent_config=new_agent_config)

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