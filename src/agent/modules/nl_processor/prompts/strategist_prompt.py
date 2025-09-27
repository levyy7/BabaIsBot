from typing import Tuple
from pathlib import Path
from src.agent.modules.nl_processor.prompts.base_prompt import BasePrompt


class StrategistPrompt(BasePrompt):
    def __init__(self, path: Path = None):
        # Initialize the parent class
        super().__init__(path)

        # Load the prompt templates from the specified path
        # self.system_template = (self.prompt_path / "strategist" / "strategist.system.md").read_text()
        self.user_template = (
            self.prompt_path / "strategist" / "strategist.user.md"
        ).read_text()

    def format(self, belief_to_test: str, current_beliefs: str) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return "", self.user_template.format(
            belief_to_test=belief_to_test, current_beliefs=current_beliefs
        )
