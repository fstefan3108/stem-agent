from stem_agent.schemas.scoring_example import ScoringExample
import json
from pathlib import Path

def load_scoring_examples(path: Path = Path("data/scoring_examples.json")) -> list[ScoringExample]:
    """Load and validate scoring examples from a JSON dataset file."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("Task example dataset must be a list.")

    if not data:
        raise ValueError("Task example dataset cannot be empty.")

    return [ScoringExample.model_validate(task_example) for task_example in data]