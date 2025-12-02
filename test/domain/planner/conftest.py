# tests/state_tests/conftest.py
import pathlib
from typing import Callable, Any

import pytest

from src.agent.state import State, Action, Block, Outcome

STATE_DIR = pathlib.Path(__file__).parent / "data" / "state_files"
STEP_DIR = pathlib.Path(__file__).parent / "data" / "step_functions"
GOAL_DIR = pathlib.Path(__file__).parent / "data" / "goal_validators"

@pytest.fixture
def load_state():
    def _load(level_id: int) -> State:
        id: str = f'{level_id if level_id >= 10 else f"0{level_id}"}'
        txt = (STATE_DIR / f'level_{id}.txt').read_text()
        return State.from_grid_string(txt)
    return _load

@pytest.fixture
def load_step_function():
    def _load(filename: str) -> Callable[[State, Action], State]:
        txt = (STEP_DIR / filename).read_text()

        local_env: dict[str, Any] = {
            "State": State,
            "Block": Block,
            "Action": Action,
            "Outcome": Outcome,
        }
        exec(txt, local_env)
        step_func: Callable[[State, Action], State] = local_env["step"]

        return step_func
    return _load


@pytest.fixture
def load_goal_validator():
    def _load(filename: str) -> Callable[[list[tuple[State, Action]], State], bool]:
        txt = (GOAL_DIR / filename).read_text()

        local_env: dict[str, Any] = {
            "State": State,
            "Block": Block,
            "Action": Action,
            "Outcome": Outcome,
        }
        exec(txt, local_env)
        goal_validator: Callable[[list[tuple[State, Action]], State], bool] = local_env["goal_validator"]

        return goal_validator

    return _load