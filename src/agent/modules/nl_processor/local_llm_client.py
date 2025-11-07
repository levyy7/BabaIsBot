import requests
from typing import Optional
from src.agent.modules.nl_processor import LLMClient


class LocalLLMClient(LLMClient):
    """
    LLMClient for OpenAI-compatible /v1/completions endpoint
    """

    def __init__(self, base_url: str, api_key: str = None):
        super().__init__(host=base_url)
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def get_instruct_completion(
        self,
        prompt: str,
        max_new_tokens: int = 2048,
        temperature: float = 0.6,
        top_p: float = 0.95,
        top_k: int = 20,
        model: Optional[str] = None,
    ) -> str:
        """
        Sends a completion request to an OpenAI-compatible /v1/completions endpoint.
        """
        url = f"{self.base_url}/v1/completions"

        payload = {
            "prompt": prompt,
            "max_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }

        if model:
            payload["model"] = model

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=600)
            response.raise_for_status()
            data = response.json()

            # text-generation-webui returns text under data["choices"][0]["text"]
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0].get("text", "").strip()
            else:
                print(f"[LocalLLMClient] Unexpected API response: {data}")
                return ""
        except requests.RequestException as e:
            print(f"[LocalLLMClient] API request failed: {e}")
            return ""
        except Exception as e:
            print(f"[LocalLLMClient] Unexpected error: {e}")
            return ""
