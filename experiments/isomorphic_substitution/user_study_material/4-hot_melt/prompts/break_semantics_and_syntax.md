You assist an AI agent in understanding the laws of an unknown world. All behavior is controlled by certain rules.

Your goal is to discover which rule has caused a discrepancy between the simulated and real state, and correct it.

### Steps:
1. Analyze the interaction of the player within the world, taking into account the performed action.
2. Compare the state discrepancies caused by the player, taking into account the rules that dictate the behavior of the environment and our current beliefs about such rules.
3. Abduct which active rule has caused the observed behavior.
4. Update or add one belief between the observed ones, using the structure below:

{
  "<Rule>": {
    "reasoning": "Why you now believe this (based on map change or behavior)",
    "description": "How does this rule affect the world?"
  }
}

### Constraints:
- Origin `(0,0)` is top-left of map.
- Try to generalize rule behavior as much as possible.
- Output only **one** belief update, modifying both the description and rationale.
- Output a valid JSON only, using the provided structure — no markdown, code blocks, or extra text.
- Explain your decision-making step by step, briefly, in `reasoning`.
- Shapes represent unknown objects.
- Colors represent unknown properties.

---

### Input:

Action Performed:
RIGHT

Map Discrepancies:
Differences at X=17,Y=8:
- pre-action              : CIRCLE
- post-action (real)      : <EMPTY>
- post-action (simulated) : <EMPTY>
Differences at X=18,Y=8:
- pre-action              : OCTAGON
- post-action (real)      : OCTAGON
- post-action (simulated) : OCTAGON,CIRCLE

Active Rules:
- GREEN X CIRCLE
- PENTAGON X RED
- HEX X YELLOW
- SQUARE X BLUE
- OCTAGON X BROWN
- CIRCLE X WHITE

Current Beliefs:
{
  "GREEN X CIRCLE": {
    "description": "The rule 'GREEN X CIRCLE' assigns the player's control to the CIRCLE object, making it the controllable entity in the game."
  },
  "HEX X YELLOW": {
    "description": "The rule 'HEX X YELLOW' sets the win condition to be met when the player-controlled entity (GREEN) touches the HEX object."
  }
}

---

Your output:
