from typing import Annotated
from pydantic import BaseModel, StringConstraints, Field


class ScoringExample(BaseModel):
    """Reference example anchoring how a response maps to coverage, grounding, and insight scores."""
    task_input: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    example_output: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    coverage: float = Field(ge=1, le=5)
    grounding: float = Field(ge=1, le=5)
    insight: float = Field(ge=1, le=5)
    coverage_rationale: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    grounding_rationale: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    insight_rationale: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]