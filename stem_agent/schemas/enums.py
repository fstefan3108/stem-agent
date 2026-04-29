from enum import Enum


class PromptSectionKey(str, Enum):
    ROLE = "role"
    STRATEGY = "strategy"
    QUALITY_CONSTRAINTS = "quality_constraints"
    OUTPUT_FORMAT = "output_format"

class ExampleQuality(str, Enum):
    GOOD = "good"
    BAD = "bad"
    EDGE_CASE = "edge_case"