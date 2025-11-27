You assist an AI agent in understanding the laws of an unknown world. All behavior is controlled by certain rules.

Your goal is to discover which rule makes the agent interact with the game and which one makes it win.

### Steps:
1. Analyze the map and rule properties.
2. Abduct which rules could be responsible for player input and win condition.
3. Induce how these rules work and what are its effects on the world.
4. Update two beliefs, using the structure below:

{{
  "<Rule_ID>": {{
    "reasoning": "Why you now believe this (based on map change or behavior)",
    "description": "How does this rule affect the world? Try ~~to generalize~~"
  }}
}}

### Constraints:
- Origin `(0,0)` is top-left of map.
- Try to generalize rule behavior as much as possible.
- Output only **two** belief update, one for the interaction and another for the win condition.
- Use **valid raw JSON only** — no markdown, code blocks, or extra text.
- Explain your decision-making step by step in `reasoning`.

---

### Input:

Active Rules:
- BABA IS YOU
- WALL IS STOP
- FLAG IS WIN
- ROCK IS PUSH

---

Your output:
