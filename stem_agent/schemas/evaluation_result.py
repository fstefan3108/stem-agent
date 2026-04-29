from typing import Annotated
from pydantic import BaseModel, StringConstraints, Field, computed_field


class EvaluationResult(BaseModel):
    """Evaluator agent output. Maps rule based improvements to the stem agent."""
    coverage: float = Field(ge=1, le=5)
    grounding: float = Field(ge=1, le=5)
    insight: float = Field(ge=1, le=5)
    feedback: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]

    @computed_field
    def total_score(self) -> float:
        return (self.coverage + self.grounding + self.insight) / 3
