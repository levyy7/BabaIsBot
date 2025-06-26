[INST]
You assist an AI agent solving turn-based puzzle levels. In this game, objects have no inherent properties. All behavior is controlled by active rules.

Your task is to generate goals with the objective of testing if a belief about a rule (predicate) is correct.

### Instructions:

1. Analyze the target belief. Identify what the predicate is expected to do and which entities it should interact with.
2. Consider scenarios where the predicate might behave unexpectedly with other rules, especially including the player itself.
3. For each goal, specify:
   - A **description** of the setup and reasoning.
   - The **expected_result** if the belief is correct.

[
  {{
    "description": "...",
    "expected_result": "..."
  }}, ...
]

### Rule Format:

The beliefs are a list of predicate descriptions, where predicates cause behaviors when used in rules:

- Structure: `<SUBJECT> IS <PREDICATE>`
- Predicate defines behavior, like movement or transformation.
- Subject references the block that the predicate affects.

Thus, blocks do not cause any interaction in the game unless there is a rule that causes them to.

### Output Format:

You must return **exactly two** goals in **raw JSON format only**, no markdown or explanation.

The format must be:
[
  {{
    "description": Step-by-step reasoning and setup, using **only generic references** like "a subject with PREDICATE" or "an entity with YOU".,
    "expected_result": The outcome that should occur if the belief is correct.
  }}, ...
]

### Constraints:
- Avoid referencing specific object names.
- Focus on rules and their interactions: refer to objects only through their assigned predicates.
- Mention clearly which predicates are active and their effects.
- Ensure all output is valid JSON with exactly two elements.

---

### Input:

Belief to Test:
{belief_to_test}

Current Beliefs:
{current_beliefs}

---

Your output:
[/INST]
