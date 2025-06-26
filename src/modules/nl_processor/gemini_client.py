import os
import time
from google import genai
from dotenv import load_dotenv, find_dotenv
from src.modules.nl_processor import LLMClient


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
            raise ValueError("Google Gemini API key must be provided or set in GEMINI_API_KEY")
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
    ) -> str:
        """
        Uses Gemini 2.0 Flash for chat-style completions.
        """

        time_since_last = time.time() - self._last_call_time
        if time_since_last < 5:
            sleep_duration = 5 - time_since_last
            print(f"Sleeping for {sleep_duration:.2f} seconds")
            time.sleep(sleep_duration)

        self._last_call_time = time.time()

        # Construct chat messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        # Call Gemini API
        response = self.client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=[system_prompt + user_prompt],
            #temperature=temperature,
            #max_output_tokens=max_tokens
        )
        # The google-genai SDK attaches output in .text
        return response.text
