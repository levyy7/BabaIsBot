import json
from collections import deque

from src.modules.memory import LongTermMemory
from src.modules.nl_processor import LLMClient

from src.models import RuleBelief
from src.modules.nl_processor.prompts.strategist_prompt import StrategistPrompt


class Strategist:
    def __init__(self, memory: LongTermMemory, client: LLMClient) -> None:
        self.memory = memory
        self.llm_client = client
        self.goal_stack = deque()


    def generate_goals_to_test_belief(self, belief_to_test: RuleBelief):
        context_beliefs = {k: v for k, v in self.memory.get_property_meanings().items()}

        system_prompt, user_prompt = StrategistPrompt().format(
            belief_to_test=str(belief_to_test),
            current_beliefs=str(context_beliefs),
        )

        print(user_prompt)

        print(context_beliefs)

        result = self.llm_client.get_completion(user_prompt=user_prompt,
                                                system_prompt=system_prompt,
                                                max_new_tokens=256,
                                                temperature=0.5)

        start = result.find('[')
        end = result.rfind(']') + 1

        json_text = result[start:end]
        try:
            json_result = json.loads(json_text)
            for value in json_result:
                print(value)

            return json_result
        except json.JSONDecodeError:
            print(f"Invalid JSON: {json_text}")
            return []