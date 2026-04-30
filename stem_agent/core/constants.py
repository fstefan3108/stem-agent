from stem_agent.schemas.enums import PromptSectionKey

REQUIRED_PROMPT_SECTION_KEYS = {
    section.value for section in PromptSectionKey
}

LOW_METRIC_TO_SECTION = {
    "coverage": "strategy",
    "grounding": "quality_constraints",
    "insight": "strategy",
}