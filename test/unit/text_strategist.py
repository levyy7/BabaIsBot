import json
import pytest
from pathlib import Path
from datetime import datetime
import time

from src.modules.core.strategist import Strategist
from src.models.rule_belief import RuleBelief
from src.modules.nl_processor import LocalLLMClient, GeminiClient
from tests.fixtures.fixtures_memory import MemoryStub, fixtures_memory_5_3


@pytest.mark.parametrize("test_id,memory_fixture_name", [
    ("main_experiment", "fixtures_memory_5_3"),
])
def test_critic_initiate_beliefs_single(test_id, memory_fixture_name, request):
    memory_fixture = request.getfixturevalue(memory_fixture_name)

    output_dir = Path("test") / "outputs" / "strategist_evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)
    # methods = ["single", "feedback", "repetition"]

    for i in range(50):
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

        memory_stub = MemoryStub(memory_fixture)
        llm_client = LocalLLMClient()

        belief_to_test = RuleBelief.from_dict("MELT", memory_stub.get_property_meanings()["MELT"])

        strategist = Strategist(memory_stub, llm_client)
        result = strategist.generate_goals_to_test_belief(belief_to_test)

        # Build descriptive filename
        filename = f"strategist_evaluation_{timestamp}.json"
        output_path = output_dir / filename

        with output_path.open("w") as f:
            json.dump({
                "test_id": test_id,
                "timestamp": timestamp,
                "iteration": i,
                "belief to test": "MELT",
                "result": result,
            }, f, indent=4)