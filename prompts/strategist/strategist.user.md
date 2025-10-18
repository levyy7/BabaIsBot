[INST]
You assist an AI agent solving a puzzle game.

Your task is to generate goals with the objective of testing if a hypothesis about the game behaviour is correct.

### Instructions:

1. Analyze the hypothesis to be tested. Reason about how new belief could interact with the existing knowledge.
2. Consider how the hypothesis and the existing knowledge could affect actions in the current state.
3. For each goal, specify:
   - A goal to test if the given hypothesis is correct, framed in the scope of the current state
   - The expected result if the belief turns out to be correct.

### Output Format:

You must return exactly two goals in raw JSON format only, no markdown or explanation.

The format must be:
[
  {{
    "goal": The goal, explained particularly for this state.
    "expected_result": The outcome that should occur if the belief is correct.
  }}, ...
]

### Constraints:
- Focus on knowledge and their interactions with the hypothesis.

---

### Input:

Hypothesis to Test:
{hypothesis}

Current Knowledge:
{knowledge}

Game State:
{state}

---

Your output:
[/INST]
