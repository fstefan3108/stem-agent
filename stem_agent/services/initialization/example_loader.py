from stem_agent.schemas.task_example import TaskExample
import json
from pathlib import Path

def load_task_examples(path: Path = Path("data/examples.json")) -> list[TaskExample]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("Task example dataset must be a list.")

    if not data:
        raise ValueError("Task example dataset cannot be empty.")

    return [TaskExample.model_validate(task_example) for task_example in data]