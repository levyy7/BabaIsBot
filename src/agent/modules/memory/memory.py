import os
import json
from typing import Any


class Memory:
    _instance = None

    memory = {}


    def __init__(self):
        if not hasattr(self, "_initialized"):  # Ensure initialization only happens once
            self._initialized = True

        self.rule_beliefs: dict[str, Any] = {}
        self.step_function: str = ""
        self.goal_condition_function: str = ""

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, "data")
        self.beliefs_path = os.path.join(self.data_dir, "beliefs.json")
        self.step_function_path = os.path.join(self.data_dir, "step_function.py")
        self.goal_condition_function_path = os.path.join(self.data_dir, "goal_condition_function.py")

        os.makedirs(self.data_dir, exist_ok=True)  # Make sure the folder exists

    def get_rule_beliefs(self) -> dict[str, Any]:
        return self.rule_beliefs

    def get_step_function(self) -> str:
        return self.step_function

    def get_goal_condition_function(self) -> str:
        return self.goal_condition_function

    def add_rule_beliefs(self, rule_beliefs: dict[str, Any]) -> None:
        lowercased_beliefs = {k.lower(): v for k, v in rule_beliefs.items()}
        self.rule_beliefs |= lowercased_beliefs
        self._save_beliefs()

    def replace_step_function(self, step_function: str) -> None:
        self.step_function = step_function
        self._save_step_function()

    def replace_goal_condition_function(self, goal_condition_function: str) -> None:
        self.goal_condition_function = goal_condition_function

        # ---------------------- Persistence ----------------------

    def _save_beliefs(self) -> None:
        """Save rule beliefs to beliefs.json"""
        with open(self.beliefs_path, "w", encoding="utf-8") as f:
            json.dump(self.rule_beliefs, f, indent=4, ensure_ascii=False)

    def _save_step_function(self) -> None:
        """Save step function code to step_function.py"""
        with open(self.step_function_path, "w", encoding="utf-8") as f:
            f.write(self.step_function)

    def _save_goal_condition_function(self) -> None:
        """Save goal condition code to goal_condition_function.py"""
        with open(self.goal_condition_function_path, "w", encoding="utf-8") as f:
            f.write(self.goal_condition_function)

    def load_beliefs(self) -> None:
        """Load beliefs.json if it exists"""
        if os.path.exists(self.beliefs_path):
            try:
                with open(self.beliefs_path, "r", encoding="utf-8") as f:
                    self.rule_beliefs = json.load(f)
            except json.JSONDecodeError:
                print("[Memory] Warning: beliefs.json is corrupted, starting empty.")

    def load_step_function(self) -> None:
        """Load step_function.py if it exists"""
        if os.path.exists(self.step_function_path):
            with open(self.step_function_path, "r", encoding="utf-8") as f:
                self.step_function = f.read()
