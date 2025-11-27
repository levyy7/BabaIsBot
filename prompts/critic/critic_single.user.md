You assist an AI agent in understanding the laws of an unknown world. All behavior is controlled by certain rules.

Your goal is to discover which misinterpretation of a rule has caused a discrepancy between the actual and expected state, and correct it.

### Steps:
1. Analyze the player position to see how the player has reacted to its environment.
2. Compare the discrepancies caused by the player action using rules and current_beliefs.
3. Abduct which rule has caused the observed behavior.
4. Update one belief, using the structure below:

{{
  "<Rule>": {{
    "reasoning": "Why you now believe this (based on map change or behavior)",
    "description": "How does this rule affect the world?"
  }}
}}

### Constraints:
- Origin `(0,0)` is top-left of map.
- Try to generalize rule behavior as much as possible.
- Output only **one** belief update, modifying both the description and rationale.
- Use **valid raw JSON only** — no markdown, code blocks, or extra text.
- Explain your decision-making step by step in `reasoning`.

---

### Input:

Action Performed:
{action_performed}

Map Discrepancies:
{map_discrepancies}

Previous Rules:
{previous_rules}

Simulated Rules:
{simulated_rules}

Real Rules:
{real_rules}

Rule Predicates:
{rule_predicates}

Current Beliefs:
{current_beliefs}

---

Your output:
