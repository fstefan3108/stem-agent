from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, computed_field, Field, StringConstraints, model_validator
from stem_agent.schemas.enums import PromptSectionKey


class EvolutionRecord(BaseModel):
    """Records the outcome of one candidate mutation attempt."""
    evolution_run_id: UUID = Field(default_factory=uuid4)
    iteration: int = Field(gt=0)
    current_config_version: int = Field(gt=0)
    candidate_config_version: int = Field(gt=0)
    current_score: float = Field(ge=1, le=5)
    candidate_score: float = Field(ge=1, le=5)
    accepted: bool
    mutation_target: PromptSectionKey
    mutation_reason: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    evaluator_feedback: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    timestamp: datetime = Field(default_factory=datetime.now)

    @computed_field
    def score_delta(self) -> float:
        return self.candidate_score - self.current_score

    @model_validator(mode="after")
    def check_versions_are_not_the_same(self):
        if self.current_config_version == self.candidate_config_version:
            raise ValueError("Current and candidate config versions must be different.")
        return self