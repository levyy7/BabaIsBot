import traceback
from typing import Dict, Callable, Any
from copy import deepcopy

from src.agent.state import State, Block, Outcome
from src.agent.state.actions import Action
from src.agent.modules.nl_processor import LLMClient
from src.agent.modules.nl_processor.prompts import BasePrompt
from src.agent.modules.memory.memory import Memory
from src.agent.modules.nl_processor.prompts.runner_prompt import (
    RunnerNewBeliefPrompt,
    RunnerErrorPrompt,
)

step_plugin_code = """
def step(state: State, action: Action) -> State:
    dx, dy = {
        Action.STILL: (0, 0),
        Action.UP: (-1, 0),
        Action.DOWN: (1, 0),
        Action.LEFT: (0, -1),
        Action.RIGHT: (0, 1),
    }[action]

    for row in state.grid:
        for cell in row:
            for block in cell:
                nx, ny = (block.x + dx, block.y + dy)  # new block position after action
                # ...

    state.outcome = Outcome.ONGOING
    return state 
"""


class Runner:
    def __init__(self, llm_client: LLMClient, memory: Memory):
        self.llm_client = llm_client
        self.memory = memory
        self.memory.replace_step_function(step_plugin_code)

    def run(self, state: State, action: Action) -> State:
        """
        Compute the next game state given current state and an action.
        """
        state_copy = deepcopy(state)
        while True:
            try:
                return self._exec_step_function(state_copy, action)
            except Exception as e:
                self._handle_step_function_error(e)

    def _exec_step_function(self, state: State, action: Action) -> State:
        """
        Dynamically execute the current step function stored in memory.
        """
        local_env: Dict[str, Any] = {
            "State": State,
            "Block": Block,
            "Action": Action,
            "Outcome": Outcome,
        }
        exec(self.memory.get_step_function(), local_env)
        step_func: Callable[[State, Action], State] = local_env["step"]
        return step_func(state, action)

    def _handle_step_function_error(self, exception: Exception) -> None:
        """
        Handle errors during step function execution and update step function.
        """
        error_messages = "\n".join(
            [
                f"[Runner] Error executing step function: {exception}",
                f"[Runner] Exception type: {type(exception).__name__}",
                f"[Runner] Exception args: {exception.args}",
                "[Runner] Traceback:",
                traceback.format_exc(),
            ]
        )
        print(error_messages)  # Replace with logging if desired
        self.update_step_function_with_error_message(error_messages)

    def update_step_function_with_new_belief(self, new_belief: str) -> None:
        """Update the step function with a new belief."""
        self._update_step_function_with_llm(
            RunnerNewBeliefPrompt(), belief_to_implement=new_belief
        )

    def update_step_function_with_error_message(self, error_message: str) -> None:
        """Update the step function to fix an error message."""
        self._update_step_function_with_llm(
            RunnerErrorPrompt(), error_message=error_message
        )

    def _update_step_function_with_llm(
        self, prompt_format: BasePrompt, **kwargs
    ) -> None:
        """
        Update the step function using the LLM based on the provided prompt format.
        """
        print("[Runner] Updating step function...")  # Replace with logging if needed
        system_prompt, user_prompt = prompt_format.format(
            step_function=self.memory.get_step_function(), **kwargs
        )

        result = self.llm_client.get_completion(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            max_new_tokens=512,
        )

        # Extract Python code block from LLM response
        start = result.find("```python") + len("```python")
        end = result.rfind("```")
        step_plugin_code = result[start:end].strip()

        self.memory.replace_step_function(step_plugin_code)
