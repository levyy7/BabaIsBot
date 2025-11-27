import json
from pathlib import Path

from src.agent.modules.nl_processor import LocalLLMClient


class BaseExperiment:
    def __init__(self, llm_host_url: str = "http://localhost:5000"):
        self.llm_client = LocalLLMClient(llm_host_url)
        self.last_result = None

    def run(self, prompt: str) -> str:
        result = self.llm_client.get_instruct_completion(
            prompt=prompt,
            temperature=0.3,
            top_p=0.7,
            top_k=30,
        )

        start, end = result.find("{"), result.rfind("}") + 1
        json_text = result[start:end]
        try:
            self.last_result = json.loads(json_text)
            return self.last_result
        except json.JSONDecodeError:
            print(f"[Critic] Invalid JSON result: {result}")
            raise json.JSONDecodeError

    def save(self, results_path: Path) -> None:
        with open(results_path, "w") as f:
            json.dump(self.last_result, f, indent=4)
