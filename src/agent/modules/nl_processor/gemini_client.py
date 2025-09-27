import os
import time
from google import genai
from dotenv import load_dotenv, find_dotenv
from src.agent.modules.nl_processor import LLMClient


load_dotenv(find_dotenv())


class GeminiClient(LLMClient):
    """
    Concrete implementation of LLMClient for Google Gemini via google-genai SDK.
    """

    def __init__(self, api_key: str = None):
        # Google Gen AI is endpoint-based, no host override
        super().__init__()
        # Retrieve API key from parameter or environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Google Gemini API key must be provided or set in GEMINI_API_KEY"
            )
        # Lazy import to avoid dependency issues
        self.client = genai.Client(api_key=self.api_key)
        self._last_call_time = time.time()

    def get_completion(
        self,
        user_prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        mode: str = "chat",
        max_new_tokens: int = 5000,
        temperature: float = 0.7,
        top_p: float = 1.0,
        model: str = "models/gemini-2.5-flash",
    ) -> str:
        """
        Uses Gemini 2.0 Flash for chat-style completions with retry logic.
        """
        print(
            f"[LLMClient] Calling to gemini API model: {model.removeprefix('models/')}"
        )

        time_since_last = time.time() - self._last_call_time
        if time_since_last < 5:
            sleep_duration = 5 - time_since_last
            print(f"Sleeping for {sleep_duration:.2f} seconds")
            time.sleep(sleep_duration)

        self._last_call_time = time.time()

        # Prepare the messages with roles properly for Gemini
        contents = user_prompt

        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents,
                    # temperature=temperature,
                    # max_output_tokens=max_new_tokens,
                    # top_p=top_p,
                )

                if response.text is None:
                    raise Exception("No response")

                return response.text
            except Exception as e:
                print(
                    f"[LLMClient] Gemini API server error on attempt {attempt + 1}/{max_retries}: {e}"
                )
                if attempt < max_retries - 1:
                    print("Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    print("Max retries reached, raising exception.")
                    raise e
        return None
