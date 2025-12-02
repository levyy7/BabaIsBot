You assist an AI agent in understanding the laws of an unknown world. All behavior is controlled by certain rules.

Your goal is to design experiments specifically intended to falsify a belief or find the specific edge cases where the belief fails.

### Instructions:

1. Identify the triggers, conditions, and resulting actions in the `belief_to_test`.
2. Look for cases which the current understanding might not be considering.
3. Design scenarios which could trigger these vulnerabilities.
4. Output the experiments, using the structure below:

[
  {{
    "description": "A high-level summary of the interaction",
    "expected_result": "The expected physical consequence"
  }}, ...
]

### Constraints:
- Output precisely {num_experiments} experiments.
- The experiments only be aimed at expanding the knowledge of the `belief to test`.
- The `description` must be an exact, reproducible sequence of steps.
- The `expected_result` should describe the specific failure state or "breaking point" you are testing for.
- Do NOT use specific grid coordinates (e.g., (x,y)) or step-by-step directional inputs.
- Origin `(0,0)` is the top-left of the map.

---

### Input:

State:
{state}

Belief to Test:
{belief_to_test}

Current Beliefs:
{current_beliefs}

Num Experiments:
{num_experiments}

---

Your output: