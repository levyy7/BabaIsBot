import requests
from typing import Optional
from src.agent.modules.nl_processor import LLMClient


class LocalLLMClient(LLMClient):
    """
    LLMClient for local inference
    """

    def __init__(self, llm_host_url: str):
        super().__init__(host=llm_host_url)
        self.headers = {"Content-Type": "application/json"}

    def get_completion(
            self,
            user_prompt: str,
            system_prompt: str = "You are a helpful assistant.",
            mode: str = "instruct",
            max_new_tokens: int = 256,
            temperature: float = 0.4,
            top_p: float = 1.0,
            model: Optional[str] = None,
    ) -> str:
        url = self.base_url
        payload = {
            "prompt": f"{system_prompt}\n{user_prompt}",
            "max_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "mode": mode,
            "stream": False,  # disables "thinking..." streaming
            "num_return_sequences": 1,  # single answer
        }
        if model:
            payload["model"] = model

        try:
            print(payload)
            response = requests.post(url, json=payload, headers=self.headers, timeout=300)
            response.raise_for_status()
            data = response.json()

            # text-generation-webui returns text in data["results"][0]["text"]
            if "results" in data and len(data["results"]) > 0:
                print(data["results"][0]["text"])
                return data["results"][0].get("text", "").strip()
            else:
                print(f"[LocalLLMClient] Unexpected API response: {data}")
                return ""
        except requests.RequestException as e:
            print(f"[LocalLLMClient] API request failed: {e}")
            return ""
        except Exception as e:
            print(f"[LocalLLMClient] Unexpected error: {e}")
            return ""