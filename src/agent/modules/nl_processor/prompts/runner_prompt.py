from typing import Tuple
from pathlib import Path
from src.agent.modules.nl_processor.prompts.base_prompt import BasePrompt


class RunnerNewBeliefPrompt(BasePrompt):
    def __init__(self, path: Path = None):
        # Initialize the parent class
        super().__init__(path)

        # Load the prompt templates from the specified path
        self.system_template = (
            self.prompt_path / "runner" / "runner_new_belief.system.md"
        ).read_text()
        self.user_template = (
            self.prompt_path / "runner" / "runner_new_belief.user.md"
        ).read_text()

    def format(self, step_function: str, belief_to_implement: str) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return self.system_template, self.user_template.format(
            step_function=step_function, belief_to_implement=belief_to_implement
        )


class RunnerErrorPrompt(BasePrompt):
    def __init__(self, path: Path = None):
        # Initialize the parent class
        super().__init__(path)

        # Load the prompt templates from the specified path
        self.system_template = (
            self.prompt_path / "runner" / "runner_error.system.md"
        ).read_text()
        self.user_template = (
            self.prompt_path / "runner" / "runner_error.user.md"
        ).read_text()

    def format(self, step_function: str, error_message: str) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return self.system_template, self.user_template.format(
            step_function=step_function, error_message=error_message
        )


class RunnerIncorrectStateTransitionPrompt(BasePrompt):
    def __init__(self, path: Path = None):
        # Initialize the parent class
        super().__init__(path)

        # Load the prompt templates from the specified path
        self.system_template = (
            self.prompt_path / "runner" / "runner_incorrect_state_transition.user.system.md"
        ).read_text()
        self.user_template = (
            self.prompt_path / "runner" / "runner_incorrect_state_transition.user.user.md"
        ).read_text()

    def format(self, belief_to_implement: str, previous_state: str, action: str, failed_state: str, correct_state: str) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return self.system_template, self.user_template.format(
            belief_to_implement=belief_to_implement, previous_state=previous_state, action=action, failed_state=failed_state, correct_state=correct_state
        )