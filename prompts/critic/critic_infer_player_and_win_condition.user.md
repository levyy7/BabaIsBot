You assist an AI agent in understanding the laws of an unknown world. All behavior is controlled by certain rules.

Your goal is to discover which rule makes the agent interact with the game and which one makes it win.

### Steps:
1. Analyze active rules, taking into account their semantic meaning.
2. Abduct which active rules could be responsible for player input and win condition.
3. Induce how these rules work and what are its effects on the world.
4. Add two new beliefs, using the structure below:

{{
  "<Rule>": {{
    "reasoning": "Why you now believe this (based on map change or behavior)",
    "description": "How does this rule affect the world?"
  }}
}}

### Constraints:
- Origin `(0,0)` is top-left of map.
- Try to generalize rule behavior as much as possible.
- Output only **two** belief update, one aimed at explaining how does player input work and another at explaining how the level is won.
- Output a valid JSON only, using the provided structure — no markdown, code blocks, or extra text.
- Explain your decision-making step by step, briefly, in `reasoning`.

---

### Input:

Active Rules:
{active_rules}

---

Your output:
