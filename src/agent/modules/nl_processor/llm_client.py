from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Abstract base class for LLM API clients.
    """

    def __init__(self, host: str = "http://localhost:5000"):
        self.base_url = host

    @abstractmethod
    def get_instruct_completion(
            self,
            prompt: str,
            max_new_tokens: int = 512,
            temperature: float = 0.6,
            top_p: float = 0.95,
            top_k: int = 20,
    ) -> str:
        """
        Abstract method: Chat-style completion. Must be implemented by subclasses.
        """
        pass
