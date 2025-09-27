import json
from typing import Dict, Any, Set

from src.agent.modules.memory.memory import Memory
from src.agent.state import State
from src.agent.modules.nl_processor import LLMClient
from src.agent.modules.nl_processor.prompts import (
    BasePrompt,
    CriticSinglePrompt,
    CriticInferPlayerAndWinCondition,
)
from src.agent.utils.prompt_utils import format_tile_diffs


class Critic:
    def __init__(self, memory: Memory, llm_client: LLMClient) -> None:
        self.memory = memory
        self.llm_client = llm_client

    def _get_rule_predicates(self, states: Set[State]) -> Set[str]:
        predicates = set()
        for state in states:
            for property_list in state.kind_to_properties.values():
                predicates.update(p.removeprefix("text_") for p in property_list)
        return predicates

    def _get_context_beliefs(self, rule_predicates: Set[str]) -> Dict[str, Any]:
        return {
            k: v
            for k, v in self.memory.get_rule_beliefs().items()
            if k in rule_predicates
        }

    def _parse_json_result(self, result: str) -> Dict[str, Any]:
        start, end = result.find("{"), result.rfind("}") + 1
        json_text = result[start:end]
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            print(f"[Critic] Invalid JSON result: {result}")
            return {}

    def _analyze(
        self,
        prompt_format: BasePrompt,
        action_performed: str,
        previous: State,
        simulated: State,
        real: State,
        **kwargs,
    ) -> Dict[str, Any]:

        player_pos = lambda state: (
            f"X={state.get_blocks_for('BABA')[0].x} Y={state.get_blocks_for('BABA')[0].y}"
            if state.get_blocks_for("BABA")
            else "destroyed"
        )
        player_position_info = (
            f"BABA - Pre-Action Position              : {player_pos(previous)}\n"
            f"     - Post-Action (simulated) Position : {player_pos(simulated)}\n"
            f"     - Post-Action (real) Position      : {player_pos(real)}"
        )

        map_discrepancies = format_tile_diffs(previous, simulated, real)
        print("[Critic] Analyzing encountered discrepancy:\n", map_discrepancies)

        rule_predicates = self._get_rule_predicates({previous, simulated, real})
        context_beliefs = self._get_context_beliefs(rule_predicates)

        system_prompt, user_prompt = prompt_format.format(
            action_performed=action_performed,
            player_position=player_position_info,
            map_discrepancies=map_discrepancies,
            previous_rules=previous.print_rules(),
            simulated_rules=simulated.print_rules(),
            real_rules=real.print_rules(),
            current_beliefs=str(context_beliefs),
            rule_predicates=str(rule_predicates),
            **kwargs,
        )

        result = self.llm_client.get_completion(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            max_new_tokens=256,
            temperature=0.5,
            model="models/gemini-2.0-flash",
        )

        json_result = self._parse_json_result(result)
        if json_result:
            self.memory.add_rule_beliefs(json_result)
        return json_result

    def analyze_single(
        self, action: str, previous: State, simulated: State, real: State
    ) -> Dict[str, Any]:
        """
        Compare simulated vs. real state and update memory with new beliefs.
        """
        return self._analyze(CriticSinglePrompt(), action, previous, simulated, real)

    def infer_player_and_win_condition(self, state: State) -> Dict[str, Any]:
        print("[Critic] Inferring Player and Win Condition...")

        rule_predicates = self._get_rule_predicates({state})
        system_prompt, user_prompt = CriticInferPlayerAndWinCondition().format(
            active_rules=state.print_rules(),
            rule_predicates=str(rule_predicates),
        )

        result = self.llm_client.get_completion(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            max_new_tokens=256,
            temperature=0.5,
        )

        json_result = self._parse_json_result(result)
        if json_result:
            self.memory.add_rule_beliefs(json_result)
        return json_result
