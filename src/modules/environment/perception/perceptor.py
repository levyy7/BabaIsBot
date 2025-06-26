from src.modules.io import BABAClient
from typing import Any, Dict


def get_state() -> Dict[str, Any]:
    return BABAClient.get("/status")