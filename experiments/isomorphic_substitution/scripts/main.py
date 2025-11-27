import json
import os
from itertools import product
from pathlib import Path

from experiments.isomorphic_substitution.scripts.base_experiment import BaseExperiment

SCENARIOS = ['0-stop', '1-defeat', '2-push', '3-sink', '4-hot_melt']
STATE_CONDITIONS = ['base', 'rephrase', 'break_semantics', 'break_syntax', 'break_semantics_and_syntax']

BASE_PATH = Path(__file__).parents[1] / 'user_study_material'
N_EXPERIMENTS_PER_SCENARIO_PER_CONDITION = 25

if __name__ == '__main__':
    base_experiment = BaseExperiment("http://192.168.0.30:5000")

    for scenario, state_condition in product(SCENARIOS, STATE_CONDITIONS):
        if scenario != '4-hot_melt':
            continue

        prompt_path = BASE_PATH / scenario / 'prompts' / f'{state_condition}.md'
        with open(prompt_path) as f:
            prompt: str = f.read()

        for i in range(N_EXPERIMENTS_PER_SCENARIO_PER_CONDITION):
            filename = f'{scenario}-{state_condition}_{i}.json'
            results_path = BASE_PATH / scenario / 'results' / state_condition / filename
            print(f"Running experiment {filename}...")

            for _ in range(5):
                try:
                    base_experiment.run(prompt)
                    break
                except Exception as e:
                    print(f"Experiment {filename} failed with error: {e}:")

            base_experiment.save(results_path)
