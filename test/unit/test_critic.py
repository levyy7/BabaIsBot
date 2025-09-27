import json
import pytest
from pathlib import Path
from datetime import datetime
import time

from src.modules.core.critic import Critic
from src.state import State
from src.modules.nl_processor import LocalLLMClient, GeminiClient
from tests.fixtures.fixtures_memory import (
    MemoryStub,
    fixtures_memory_0_0,
    fixtures_memory_4_0,
    fixtures_memory_4_1,
    fixtures_memory_5_0,
    fixtures_memory_5_1,
    fixtures_memory_5_3,
)
from tests.fixtures.fixtures_state import (
    DummyState,
    fixtures_state_0_0,
    fixtures_state_4_0,
    fixtures_state_4_1,
    fixtures_state_5_0,
    fixtures_state_5_1,
    fixtures_state_5_2,
)


@pytest.mark.parametrize(
    "test_id,action,memory_fixture_name,state_fixture_name",
    [
        # ("unexpected_wall_hit", "MOVE_DOWN", "fixtures_memory_0_0", "fixtures_state_0_0"),
        # ("unexpected_defeat", "MOVE RIGHT", "fixtures_memory_4_0", "fixtures_state_4_0"),
        # ("unexpected_chain_push", "MOVE UP", "fixtures_memory_4_1", "fixtures_state_4_1"),
        (
            "unexpected_hot_melt",
            "MOVE RIGHT",
            "fixtures_memory_5_0",
            "fixtures_state_5_0",
        ),
        # ("unexpected_rock_to_lava", "MOVE LEFT", "fixtures_memory_5_1", "fixtures_state_5_1"),
        # ("main_experiment", "MOVE RIGHT", "fixtures_memory_5_3", "fixtures_state_5_2"),
    ],
)
def test_critic_initiate_beliefs_single(
    test_id, action, memory_fixture_name, state_fixture_name, request
):
    memory_fixture = request.getfixturevalue(memory_fixture_name)
    state_fixture = request.getfixturevalue(state_fixture_name)

    output_dir = Path("test") / "outputs" / "critic_prompt_method_evaluation" / "single"
    output_dir.mkdir(parents=True, exist_ok=True)
    # methods = ["single", "feedback", "repetition"]

    for i in range(1):
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        previous_dict, expected_dict, actual_dict = state_fixture

        memory_stub = MemoryStub(memory_fixture)
        llm_client = LocalLLMClient()
        critic = Critic(memory_stub, llm_client)

        previous = State.from_dict(previous_dict)
        expected = State.from_dict(expected_dict)
        actual = State.from_dict(actual_dict)

        result = critic.analyze_single(action, previous, expected, actual)

        # Build descriptive filename
        filename = f"single_{test_id}_{timestamp}.json"
        output_path = output_dir / filename

        # Save result
        with output_path.open("w") as f:
            json.dump(
                {
                    "test_id": test_id,
                    "timestamp": timestamp,
                    "iteration": i,
                    "action": action,
                    "result": result,
                },
                f,
                indent=4,
            )


@pytest.mark.parametrize(
    "test_id,action,memory_fixture_name,state_fixture_name",
    [
        (
            "unexpected_wall_hit",
            "MOVE_DOWN",
            "fixtures_memory_0_0",
            "fixtures_state_0_0",
        ),
        (
            "unexpected_defeat",
            "MOVE RIGHT",
            "fixtures_memory_4_0",
            "fixtures_state_4_0",
        ),
        (
            "unexpected_chain_push",
            "MOVE UP",
            "fixtures_memory_4_1",
            "fixtures_state_4_1",
        ),
        (
            "unexpected_hot_melt",
            "MOVE RIGHT",
            "fixtures_memory_5_0",
            "fixtures_state_5_0",
        ),
        (
            "unexpected_rock_to_lava",
            "MOVE LEFT",
            "fixtures_memory_5_1",
            "fixtures_state_5_1",
        ),
    ],
)
def test_critic_initiate_beliefs_feedback(
    test_id, action, memory_fixture_name, state_fixture_name, request
):
    memory_fixture = request.getfixturevalue(memory_fixture_name)
    state_fixture = request.getfixturevalue(state_fixture_name)

    output_dir = (
        Path("test") / "outputs" / "critic_prompt_method_evaluation" / "feedback"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    # methods = ["single", "feedback", "repetition"]

    for i in range(10):
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        previous_dict, expected_dict, actual_dict = state_fixture

        memory_stub = MemoryStub(memory_fixture)
        llm_client = GeminiClient()
        critic = Critic(memory_stub, llm_client)

        previous = State.from_dict(previous_dict)
        expected = State.from_dict(expected_dict)
        actual = State.from_dict(actual_dict)

        result = critic.analyze_feedback(action, previous, expected, actual, 3)

        # Build descriptive filename
        filename = f"feedback_{test_id}_{timestamp}.json"
        output_path = output_dir / filename

        # Save result
        with output_path.open("w") as f:
            json.dump(
                {
                    "test_id": test_id,
                    "timestamp": timestamp,
                    "iteration": i,
                    "action": action,
                    "result": result,
                },
                f,
                indent=4,
            )


@pytest.mark.parametrize(
    "test_id,action,memory_fixture_name,state_fixture_name",
    [
        (
            "unexpected_wall_hit",
            "MOVE_DOWN",
            "fixtures_memory_0_0",
            "fixtures_state_0_0",
        ),
        (
            "unexpected_defeat",
            "MOVE RIGHT",
            "fixtures_memory_4_0",
            "fixtures_state_4_0",
        ),
        (
            "unexpected_chain_push",
            "MOVE UP",
            "fixtures_memory_4_1",
            "fixtures_state_4_1",
        ),
        (
            "unexpected_hot_melt",
            "MOVE RIGHT",
            "fixtures_memory_5_0",
            "fixtures_state_5_0",
        ),
        (
            "unexpected_rock_to_lava",
            "MOVE LEFT",
            "fixtures_memory_5_1",
            "fixtures_state_5_1",
        ),
    ],
)
def test_critic_initiate_beliefs_repetition(
    test_id, action, memory_fixture_name, state_fixture_name, request
):
    memory_fixture = request.getfixturevalue(memory_fixture_name)
    state_fixture = request.getfixturevalue(state_fixture_name)

    output_dir = (
        Path("test") / "outputs" / "critic_prompt_method_evaluation" / "repetition"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    # methods = ["single", "feedback", "repetition"]

    for i in range(10):
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        previous_dict, expected_dict, actual_dict = state_fixture

        memory_stub = MemoryStub(memory_fixture)
        llm_client = LocalLLMClient()
        critic = Critic(memory_stub, llm_client)

        previous = State.from_dict(previous_dict)
        expected = State.from_dict(expected_dict)
        actual = State.from_dict(actual_dict)

        result = critic.analyze_repetition(action, previous, expected, actual, 3)

        # Build descriptive filename
        filename = f"repetition_{test_id}_{timestamp}.json"
        output_path = output_dir / filename

        # Save result
        with output_path.open("w") as f:
            json.dump(
                {
                    "test_id": test_id,
                    "timestamp": timestamp,
                    "iteration": i,
                    "action": action,
                    "result": result,
                },
                f,
                indent=4,
            )
