import requests
from src.agent.modules.nl_processor import LLMClient


class LocalLLMClient(LLMClient):
    """
    Concrete implementation of LLMClient for a local server.
    """

    def __init__(self, llm_host_url: str):
        super().__init__(host=llm_host_url)

    def get_completion(
        self,
        user_prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        mode: str = "instruct",
        max_new_tokens: int = 256,
        temperature: float = 0.4,
        top_p: float = 1.0,
        model: str = None,
    ) -> str:
        url = f"{self.base_url}"
        payload = {
            "prompt": user_prompt,
            "max_tokens": max_new_tokens,
            "temperature": temperature,
        }
        # headers = {"Content-Type": "application/json"}

        try:
            print("i reach 1")
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            print("[DEBUG] Response JSON:", data)
            return data["choices"][0]["text"]
        except Exception as e:
            print(f"[LocalLLMClient] API error: {e}")
            return ""

