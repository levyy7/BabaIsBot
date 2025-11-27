from typing import Tuple
from pathlib import Path
from src.agent.modules.nl_processor.prompts.base_prompt import BasePrompt


class CriticSinglePrompt(BasePrompt):
    def __init__(self, path: Path = None):
        # Initialize the parent class
        super().__init__(path)

        # Load the prompt templates from the specified path
        self.system_template = (
            self.prompt_path / "critic" / "critic_single.system.md"
        ).read_text()
        self.user_template = (
            self.prompt_path / "critic" / "critic_single.user.md"
        ).read_text()

    def format(
        self,
        action: str,
        map_discrepancies: str,
        active_rules: str,
        current_beliefs: str,
    ) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return self.system_template, self.user_template.format(
            action=action,
            map_discrepancies=map_discrepancies,
            active_rules=active_rules,
            current_beliefs=current_beliefs,
        )


class CriticInferPlayerAndWinCondition(BasePrompt):
    def __init__(self, path: Path = None):
        # Initialize the parent class
        super().__init__(path)

        # Load the prompt templates from the specified path
        self.system_template = (
            self.prompt_path
            / "critic"
            / "critic_infer_player_and_win_condition.system.md"
        ).read_text()
        self.user_template = (
            self.prompt_path
            / "critic"
            / "critic_infer_player_and_win_condition.user.md"
        ).read_text()

    def format(self, active_rules: str) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return self.system_template, self.user_template.format(
            active_rules=active_rules
        )
