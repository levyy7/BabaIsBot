import requests
import re
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

    def _clean_and_repair_json(self, text: str) -> str:
        """
        Extracts JSON from markdown code blocks and attempts to fix
        common model errors (like missing quotes on keys).
        """
        # 1. Extract content inside ```json ... ``` or ``` ... ```
        code_block_pattern = r"```(?:json)?\s*(.*?)\s*```"
        match = re.search(code_block_pattern, text, re.DOTALL)

        if match:
            clean_text = match.group(1)
        else:
            # Fallback: Attempt to find the first open brace { and last close brace }
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                clean_text = text[start: end + 1]
            else:
                clean_text = text  # Return original if no structure found

        # 2. Attempt to fix the specific error: Missing opening quote on keys
        # Finds:  movement_blocked": true
        # Replaces with: "movement_blocked": true
        # Regex explanation: Look for word chars followed by ": but NOT preceded by "
        clean_text = re.sub(r'(?<=[\{\,])\s*([a-zA-Z0-9_]+)(\":)', r' "\1\2', clean_text)

        return clean_text.strip()

    def get_instruct_completion(
            self,
            prompt: str,
            max_new_tokens: int = 2048,
            temperature: float = 0.6,
            top_p: float = 0.95,
            top_k: int = 20,
            model: Optional[str] = None,
    ) -> str:

        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "mode": "instruct",
            "max_tokens": 300,  # Reduced to prevent massive thinking loops
            "repetition_penalty": 1.15,
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

            if "choices" in data and len(data["choices"]) > 0:
                raw_content = data["choices"][0].get("message", {}).get("content", "")

                # --- APPLY THE FIX HERE ---
                clean_json_string = self._clean_and_repair_json(raw_content)
                return clean_json_string
            else:
                print(f"[LocalLLMClient] Unexpected API response: {data}")
                return "{}"  # Return empty valid JSON on failure

        except requests.RequestException as e:
            print(f"[LocalLLMClient] API request failed: {e}")
            return "{}"
        except Exception as e:
            print(f"[LocalLLMClient] Unexpected error: {e}")
            return "{}"