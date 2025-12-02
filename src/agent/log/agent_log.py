from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any


@dataclass
class AgentLog:
    prompt_number: int
    level_id: int
    level_name: str
    model_name: str
    module: str
    goal_queue: list[dict[str, Any]]
    current_goal_function: str
    current_beliefs: dict[str, Any]
    current_step_function: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary, formatting the
        timestamp as a string for JSON serialization.
        """
        data = asdict(self)
        # Convert datetime object to ISO string format
        data['timestamp'] = self.timestamp.isoformat()
        return data