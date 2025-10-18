import json
from collections import deque
from typing import Any

from src.agent.modules.memory.memory import Memory
from src.agent.modules.nl_processor import LLMClient

from src.agent.modules.nl_processor.prompts.strategist_prompt import StrategistPrompt
from src.agent.state import State, Outcome


class Strategist:
    def __init__(self, memory: Memory, llm_client: LLMClient) -> None:
        self.memory = memory
        self.llm_client = llm_client
        self.goal_stack = deque()

        self.default_goal_function = (lambda s : s.outcome == Outcome.WIN)

    def get_next_goal(self):
        if self.goal_stack:
            return self.goal_stack.pop()

        return None

    def generate_goals_to_test_hypothesis(self, state: State, hypothesis: str):
        context_beliefs = self._get_context_beliefs(self._get_rule_predicates({state}))

        system_prompt, user_prompt = StrategistPrompt().format(
            hypothesis=hypothesis,
            knowledge=str(context_beliefs),
            state=str(state)
        )

        print(user_prompt)

        print(context_beliefs)

        result = self.llm_client.get_completion(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
        )

        start = result.find("[")
        end = result.rfind("]") + 1

        json_text = result[start:end]
        try:
            json_result = json.loads(json_text)
            for value in json_result:
                print(value)

            return json_result
        except json.JSONDecodeError:
            print(f"Invalid JSON: {json_text}")
            return []


    def _get_rule_predicates(self, states: set[State]) -> set[str]:
        predicates = set()
        for state in states:
            for property_list in state.kind_to_properties.values():
                predicates.update(p.removeprefix("text_") for p in property_list)
        return predicates

    def _get_context_beliefs(self, rule_predicates: set[str]) -> dict[str, Any]:
        return {
            k: v
            for k, v in self.memory.get_rule_beliefs().items()
            if k in rule_predicates
        }