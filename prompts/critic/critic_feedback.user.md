[INST]
You assist an AI agent solving turn-based puzzle levels. In this game, objects have no inherent properties. All behavior is controlled by active rules.

Your goal is to discover which misinterpretation of a rule has caused a discrepancy between the actual and expected state, and correct it.

This prompt is part of a feedback refinement loop. You are provided with the belief update from the last iteration in {last_iteration_output}. Your task is to refine or improve that belief update to better explain the discrepancy and clarify the predicate's behavior.

Follow these steps:
1. Review `Last Iteration Output` to understand the previous belief and rationale.
2. Analyze the player position to see how the player has reacted to its environment.
3. Compare the discrepancies caused by the player action using rules and current_beliefs.
4. Decide whether to keep the same predicate or switch to a better-fitting one from the `Rule Predicates` list.
5. Output exactly one refined predicate belief, using this structure:

{{
  "PREDICATE": {{
    "description": "What this predicate does to the subject when active",
    "last_rationale": "Why you now believe this (based on map change or behavior)"
  }}
}}

---

### Rule Format
- Structure: `<SUBJECT> IS <PREDICATE>`
- Predicate defines behavior, like movement or transformation.
- Subject references the block that the predicate affects.

Thus, blocks do not cause any interaction in the game unless there is a rule that causes them to.

---

### Constraints:
- Origin `(0,0)` is top-left of map.
- Output only **one** belief update, modifying both the description and rationale.
- Choose the updated predicate from the `Rule Predicates` list below.
- Use **valid raw JSON only** — no markdown, code blocks, or extra text.
- Explain your decision-making step by step in `last_rationale`.

---

### Input:

Action Performed:
{action_performed}

Player Position:
{player_position}

Map Discrepancies:
{map_discrepancies}

Previous Rules:
{previous_rules}

Expected Rules:
{expected_rules}

Actual Rules:
{actual_rules}

Rule Predicates:
{rule_predicates}

Current Beliefs:
{current_beliefs}

Last Iteration Output:
{last_iteration}
---

### Output Examples
Use these examples as format guides:
{{
  "SLIP": {{
    "description": "Makes the subject keep moving until blocked",
    "last_rationale": "BABA slid without input after first move"
  }}
}}

---

Your output:
[/INST]
