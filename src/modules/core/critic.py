import json
from typing import Dict, Any

from src.modules.memory import LongTermMemory
from src.state import State
from src.modules.nl_processor import LLMClient
from src.modules.nl_processor.prompts import BasePrompt, CriticSinglePrompt, CriticFeedbackPrompt, CriticRepetitionPrompt
from src.utils.state_utils import diff_states
from src.utils.prompt_utils import format_tile_diffs


class Critic:
    def __init__(self, memory: LongTermMemory, client: LLMClient) -> None:
        self.memory = memory
        self.llm_client = client

    def _analyze(self, prompt_format: BasePrompt, action_performed: str, previous: State, expected: State, actual: State, **kwargs) -> Dict[str, Any]:
        diff = diff_states(expected, actual)

        player_position = f"""
            BABA (Initial Position: {f"X={previous.to_dict()['blocks']['BABA'][0]['x']} Y={previous.to_dict()['blocks']['BABA'][0]['y']}" if 'BABA' in previous.to_dict()['blocks'] else "non-existent"}):
                Expected Position:  {f"X={expected.to_dict()['blocks']['BABA'][0]['x']} Y={expected.to_dict()['blocks']['BABA'][0]['y']}" if 'BABA' in expected.to_dict()['blocks'] else "destroyed"}
                Actual Position:  {f"X={actual.to_dict()['blocks']['BABA'][0]['x']} Y={actual.to_dict()['blocks']['BABA'][0]['y']}" if 'BABA' in actual.to_dict()['blocks'] else "destroyed"}
        """.strip()

        map_discrepancies = format_tile_diffs(diff["tiles"], previous)

        rule_predicates = {
            item["object"]
            for data_dict in [previous.to_dict(), expected.to_dict(), actual.to_dict()]
            if "rules" in data_dict  # Ensure "rules" key exists
            for rule_list in data_dict["rules"].values()
            for item in rule_list
            if "object" in item and item["object"] != 'YOU' and item["object"] != 'WIN' # Ensure "object" key exists
        }
        context_beliefs = {k: v for k, v in self.memory.get_property_meanings().items() if k in rule_predicates}

        system_prompt, user_prompt = prompt_format.format(
            action_performed=action_performed,
            player_position=player_position,
            map_discrepancies=map_discrepancies,
            previous_rules=str(previous.to_dict_compressed()["rules"]),
            expected_rules=str(expected.to_dict_compressed()["rules"]),
            actual_rules=str(actual.to_dict_compressed()["rules"]),
            current_beliefs=str(context_beliefs),
            rule_predicates=str(rule_predicates),
            **kwargs
        )

        print(user_prompt)

        print(context_beliefs)

        result = self.llm_client.get_completion(user_prompt=user_prompt,
                                                system_prompt=system_prompt,
                                                max_new_tokens=256,
                                                temperature=0.5)

        start = result.find('{')
        end = result.rfind('}') + 1

        json_text = result[start:end]
        try:
            json_result = json.loads(json_text)
            return json_result
        except json.JSONDecodeError:
            print(f"Invalid JSON: {result}")
            return {}

    def analyze_single(self, action_performed: str, previous: State, expected: State, actual: State) -> Dict[str, Any]:
        """
        Compare expected vs. actual state and return update memory with new beliefs.
        """
        return self._analyze(CriticSinglePrompt(), action_performed, previous, expected, actual)

    def analyze_feedback(self, action_performed: str, previous: State, expected: State, actual: State, iterations: int) -> Dict[str, Any]:
        last_iteration = self._analyze(CriticSinglePrompt(), action_performed, previous, expected, actual)
        for i in range(iterations - 1):
            print(last_iteration)
            last_iteration = self._analyze(CriticFeedbackPrompt(), action_performed, previous, expected, actual, last_iteration=last_iteration)
        return last_iteration

    def analyze_repetition(self, action_performed: str, previous: State, expected: State, actual: State, iterations: int) -> Dict[str, Any]:
        iteration_list = []
        for i in range(iterations - 1):
            iteration_list.append(self._analyze(CriticSinglePrompt(), action_performed, previous, expected, actual))

        return self._analyze(CriticRepetitionPrompt(), action_performed, previous, expected, actual, iteration_list=iteration_list)