import pytest

from src.agent.modules.core.planner.bfs_planner import BFSPlanner
from src.agent.modules.core.planner.iw_planner import IWPlanner

LEVEL_IDS = [0, 1, 2, 3, 4, 5, 6]
STEP_FUNCTION_NAME = 'step_05.txt'
GOAL_VALIDATOR_NAME = 'default.txt'

@pytest.mark.parametrize("level_id", LEVEL_IDS)
def test_bfs_reaches_goal(level_id, load_state, load_step_function, load_goal_validator):
    state = load_state(level_id)
    step_function = load_step_function(STEP_FUNCTION_NAME)
    goal_validator = load_goal_validator(GOAL_VALIDATOR_NAME)

    planner = BFSPlanner(step_function, goal_validator)
    plan = planner.plan(state)

    assert plan is not None


@pytest.mark.parametrize("level_id", LEVEL_IDS)
def test_iw_reaches_goal(level_id, load_state, load_step_function, load_goal_validator):
    state = load_state(level_id)
    step_function = load_step_function(STEP_FUNCTION_NAME)
    goal_validator = load_goal_validator(GOAL_VALIDATOR_NAME)

    planner = IWPlanner(step_function, goal_validator)
    plan = planner.plan(state)

    assert plan is not None