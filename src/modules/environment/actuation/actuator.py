from src.modules.io import BABAClient
from src.environment.actuation.action_type import ActionType
from typing import Any, Dict


def send_action(action: ActionType, payload: Dict[str, Any] = None) -> None:
    endpoint = ""

    match action:
        case action.is_movement():
            endpoint = f"/move/{action.name.lower()}"
        case action.is_level_modifier():
            endpoint = f"/level/{action.name.lower()}"
        case action.EXIT:
            endpoint = "/exit"

    BABAClient.post(endpoint, payload)