from textwrap import dedent
from langchain_openai import ChatOpenAI

from stem_agent.core.settings import settings
from stem_agent.schemas.agent_config import AgentConfig
from stem_agent.schemas.prompt_section import RefinedPromptSections, PromptSection
from stem_agent.schemas.task_example import TaskExample


class AgentConfigRefinementEngine:
    def __init__(self, current_config: AgentConfig, task_examples: list[TaskExample]):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.CONFIG_REFINER_MODEL,
            temperature=0
        ).with_structured_output(RefinedPromptSections, method="function_calling")
        self.current_config = current_config
        self.task_examples = task_examples

    def generate_refined_agent_config(self) -> AgentConfig:
        refined_prompt_sections = self._create_refined_prompt_sections()
        return AgentConfig(
            task_class="deep_research",
            available_tools=[],
            prompt_sections={
                "role": PromptSection(content=refined_prompt_sections.role),
                "strategy": PromptSection(content=refined_prompt_sections.strategy),
                "quality_constraints": PromptSection(content=refined_prompt_sections.quality_constraints),
                "output_format": PromptSection(content=refined_prompt_sections.output_format),
            },
            version=self.current_config.version + 1,
            created_from="initialized_from_examples"
        )

    def _create_refined_prompt_sections(self) -> RefinedPromptSections:
        prompt = self._build_prompt()
        return self.llm.invoke(prompt)

    def _build_prompt(self) -> str:
        formatted_examples = self._format_examples()
        return dedent(f"""
You are analyzing examples of deep research outputs to improve an AI agent's prompt configuration.

CURRENT PROMPT CONFIGURATION:
Role: {self.current_config.prompt_sections["role"].content}
Strategy: {self.current_config.prompt_sections["strategy"].content}
Quality Constraints: {self.current_config.prompt_sections["quality_constraints"].content}
Output Format: {self.current_config.prompt_sections["output_format"].content}

EXAMPLES TO ANALYZE:
{formatted_examples}

TASK:
Study the examples above. Identify what separates the good examples from the bad ones.
Do NOT copy instructions from the examples — infer the patterns yourself.
Then rewrite each of the four prompt sections to reflect what makes a good deep research response.

RULES:
- Rewrite all four sections: role, strategy, quality_constraints, output_format
- Each section must be specific and actionable — no vague instructions
- Base your changes entirely on patterns you observe in the examples
- Do not mention specific frameworks or topics from the examples
        """).strip()

    def _format_examples(self) -> str:
        examples_text = ""
        for i, example in enumerate(self.task_examples, 1):
            examples_text += f"""
        Example {i} [{example.quality_label.value.upper()}]:
        Task: {example.task_input}
        Output: {example.example_output}
        Notes: {chr(10).join(f'- {note}' for note in example.notes)}
        ---"""
        return examples_text
