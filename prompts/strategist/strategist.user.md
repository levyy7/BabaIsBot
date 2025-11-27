[INST]
You assist an AI agent in understanding the laws of an unknown world. All behavior is controlled by certain rules.

Your task is to generate goals with the objective of testing if a belief about a rule (predicate) is correct.

### Instructions:

1. Analyze the target belief, understand what the behaviour of the rule is.
2. Understand how this rule affects the current environment, and what possible effects could it lead to.
3. Consider scenarios where the predicate might behave unexpectedly with other rules, especially including the player itself.
4. For each goal, use the following structure:

[
  {{
    "description": "A description of the experiment setup, explaining step-by-step how to reproduce it.",
    "expected_result": "What are you expecting to happen?"
  }}, ...
]

### Constraints:
- Origin `(0,0)` is top-left of map.
- Explain your decision-making.
- Focus on rules and their interactions.
- Output a valid JSON only, using the provided structure — no markdown, code blocks, or extra text.

---

### Input:

State:
{state}

Belief to Test:
{belief_to_test}

Current Beliefs:
{current_beliefs}

---

Your output:
[/INST]
