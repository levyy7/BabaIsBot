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
        action_performed: str,
        player_position: str,
        map_discrepancies: str,
        previous_rules: str,
        simulated_rules: str,
        real_rules: str,
        current_beliefs: str,
        rule_predicates: str,
    ) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return self.system_template, self.user_template.format(
            action_performed=action_performed,
            player_position=player_position,
            map_discrepancies=map_discrepancies,
            previous_rules=previous_rules,
            simulated_rules=simulated_rules,
            real_rules=real_rules,
            current_beliefs=current_beliefs,
            rule_predicates=rule_predicates,
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

    def format(self, active_rules: str, rule_predicates: str) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return self.system_template, self.user_template.format(
            active_rules=active_rules, rule_predicates=rule_predicates
        )


class CriticFeedbackPrompt(BasePrompt):
    def __init__(self, path: Path = None):
        # Initialize the parent class
        super().__init__(path)

        # Load the prompt templates from the specified path
        self.system_template = (
            self.prompt_path / "critic" / "critic_feedback.system.md"
        ).read_text()
        self.user_template = (
            self.prompt_path / "critic" / "critic_feedback.user.md"
        ).read_text()

    def format(
        self,
        action_performed: str,
        player_position: str,
        map_discrepancies: str,
        previous_rules: str,
        expected_rules: str,
        actual_rules: str,
        current_beliefs: str,
        rule_predicates: str,
        last_iteration: str,
    ) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return "", self.user_template.format(
            action_performed=action_performed,
            player_position=player_position,
            map_discrepancies=map_discrepancies,
            previous_rules=previous_rules,
            expected_rules=expected_rules,
            actual_rules=actual_rules,
            current_beliefs=current_beliefs,
            rule_predicates=rule_predicates,
            last_iteration=last_iteration,
        )


class CriticRepetitionPrompt(BasePrompt):
    def __init__(self, path: Path = None):
        # Initialize the parent class
        super().__init__(path)

        # Load the prompt templates from the specified path
        self.system_template = (
            self.prompt_path / "critic" / "critic_repetition.system.md"
        ).read_text()
        self.user_template = (
            self.prompt_path / "critic" / "critic_repetition.user.md"
        ).read_text()

    def format(
        self,
        action_performed: str,
        player_position: str,
        map_discrepancies: str,
        previous_rules: str,
        expected_rules: str,
        actual_rules: str,
        current_beliefs: str,
        rule_predicates: str,
        iteration_list: str,
    ) -> Tuple[str, str]:
        # Format the prompt templates with the provided arguments
        return "", self.user_template.format(
            action_performed=action_performed,
            player_position=player_position,
            map_discrepancies=map_discrepancies,
            previous_rules=previous_rules,
            expected_rules=expected_rules,
            actual_rules=actual_rules,
            current_beliefs=current_beliefs,
            rule_predicates=rule_predicates,
            iteration_list=iteration_list,
        )
