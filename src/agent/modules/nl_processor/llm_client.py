from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Abstract base class for LLM API clients.
    """

    def __init__(self, host: str = "http://localhost:5000"):
        self.base_url = host

    @abstractmethod
    def get_completion(
        self,
        user_prompt: str,
        system_prompt: str,
        mode: str = "chat",
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 1.0,
        model: str = "models/gemini-2.5-flash",
    ) -> str:
        """
        Abstract method: Chat-style completion. Must be implemented by subclasses.
        """
        pass
