from textwrap import dedent

from stem_agent.schemas.scoring_example import ScoringExample


def build_evaluator_prompt(user_task: str, stem_agent_answer: str, scoring_examples: list[ScoringExample]) -> str:
    formatted_examples = _format_examples(scoring_examples)
    return dedent(f"""
You are evaluating the quality of a deep research response against a reference dataset of scored examples.

ORIGINAL TASK:
{user_task}

AGENT'S RESPONSE:
{stem_agent_answer}

REFERENCE EXAMPLES:
{formatted_examples}

EVALUATION INSTRUCTIONS:

For each metric, find the reference example whose response most closely matches the agent's response in quality. Use that example's score for that metric as your anchor.

METRICS:

1. COVERAGE — Did the response address all aspects implied by the task?
2. GROUNDING — Are claims supported with specific evidence, named entities, or concrete details?
3. INSIGHT — Does the response transform information into decision-useful analysis (comparisons, tradeoffs, recommendations)?

SCORING:
- Use the full 1.0 to 5.0 range, not just integers
- Anchor each score to the closest reference example for that metric
- Do not use your own opinion — use the reference scores as the standard
- A response with structure but no real depth should score in the 2-3 range, not 4-5

OUTPUT:
Score each metric and provide one feedback sentence per metric explaining which reference example you anchored to and why.
        """).strip()

def _format_examples(scoring_examples: list[ScoringExample]) -> str:
        examples_text = ""
        for i, example in enumerate(scoring_examples, 1):
            examples_text += dedent(f"""
    Example {i}:
    Task: {example.task_input}
    Response: {example.example_output}

    Scores:
    - Coverage: {example.coverage} — {example.coverage_rationale}
    - Grounding: {example.grounding} — {example.grounding_rationale}
    - Insight: {example.insight} — {example.insight_rationale}
    ---""")
        return examples_text