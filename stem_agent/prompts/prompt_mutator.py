from textwrap import dedent


def build_mutator_prompt(
    current_section_content: str,
    target_section_name: str,
    weak_metric: str,
    evaluator_feedback: str
) -> str:
    return dedent(f"""
You are improving one section of an AI agent's prompt configuration.

The agent was evaluated and scored low on the metric: {weak_metric}.

EVALUATOR FEEDBACK:
{evaluator_feedback}

SECTION BEING REWRITTEN: {target_section_name}

CURRENT CONTENT OF THIS SECTION:
{current_section_content}

YOUR TASK:
Rewrite the content of this section to specifically address the weakness identified by the evaluator.

RULES:
- Output only the new section content as plain text — no headers, no labels, no explanation
- Keep the rewrite focused on improving the {weak_metric} metric
- Do not change the section's purpose, only how it instructs the agent
- Be specific and actionable — vague instructions will not improve the score
- Do not mention specific topics, frameworks, or domains — keep instructions general
- Make a small, focused improvement to the selected section
- Do not rewrite the entire section into an expert-level instruction
""").strip()