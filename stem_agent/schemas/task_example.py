from typing import Annotated
from pydantic import BaseModel, StringConstraints

from stem_agent.schemas.enums import ExampleQuality


class TaskExample(BaseModel):
    task_input: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    example_output: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    quality_label: ExampleQuality
    notes: list[Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]]