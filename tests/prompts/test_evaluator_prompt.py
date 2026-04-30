from stem_agent.prompts.evaluator import build_evaluator_prompt
from stem_agent.schemas.scoring_example import ScoringExample


def test_evaluator_prompt_contains_inputs_and_examples():
    examples = [
        ScoringExample(
            task_input="Research X.",
            example_output="X is a thing.",
            coverage=2.0,
            grounding=2.5,
            insight=2.0,
            coverage_rationale="Shallow coverage rationale.",
            grounding_rationale="Vague grounding rationale.",
            insight_rationale="No analysis rationale."
        )
    ]
    prompt = build_evaluator_prompt(
        user_task="Research the latest AI frameworks.",
        stem_agent_answer="There are many frameworks.",
        scoring_examples=examples
    )

    assert "Research the latest AI frameworks." in prompt
    assert "There are many frameworks." in prompt
    assert "Research X." in prompt
    assert "Shallow coverage rationale." in prompt