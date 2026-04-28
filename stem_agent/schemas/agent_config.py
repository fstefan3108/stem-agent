from typing import Annotated
from pydantic import BaseModel, Field, model_validator, StringConstraints
from stem_agent.schemas.prompt_section import PromptSection
from stem_agent.core.constants import REQUIRED_PROMPT_SECTION_KEYS


class AgentConfig(BaseModel):
    """Represents the full configurable genome of a stem agent throughout its lifecycle."""
    task_class: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    available_tools: list[str] = Field(default_factory=list)
    prompt_sections: dict[str, PromptSection]
    max_steps: int = Field(default=1, ge=1, le=10)
    version: int = Field(default=1, ge=1)
    stages: list[str] = Field(default_factory=list)
    created_from: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]

    @model_validator(mode="after")
    def validate_prompt_sections(self):
        section_keys = set(self.prompt_sections.keys())
        if section_keys != REQUIRED_PROMPT_SECTION_KEYS:
            missing_keys = REQUIRED_PROMPT_SECTION_KEYS - section_keys
            extra_keys = section_keys - REQUIRED_PROMPT_SECTION_KEYS
            raise ValueError(f"Invalid section keys - missing: {missing_keys}\nextra: {extra_keys}")
        return self