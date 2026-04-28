from typing import Annotated
from pydantic import BaseModel, Field, model_validator, StringConstraints


class PromptSection(BaseModel):
    """Represents a single section inside an evolving adaptable prompt."""
    content: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    version: int = Field(default=1, ge=1)

    mutable: bool = True
    mutation_reason: str | None = None

    @model_validator(mode="after")
    def require_mutation_reason_for_mutated_sections(self):
        if not self.mutable and self.version > 1:
            raise ValueError("Non-mutable sections cannot have version greater than 1.")

        if not self.mutable and self.mutation_reason is not None:
            raise ValueError("Non-mutable sections cannot have a mutation reason.")

        if self.version > 1 and self.mutation_reason is None:
            raise ValueError("A mutation reason must be provided when version is greater than 1.")

        return self
