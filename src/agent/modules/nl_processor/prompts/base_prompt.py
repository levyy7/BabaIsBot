from typing import Tuple
from abc import ABC, abstractmethod
from pathlib import Path


class BasePrompt(ABC):
    @abstractmethod
    def __init__(self, path: Path = None):
        if path is not None:
            self.prompt_path = path
        else:
            self.prompt_path = Path(__file__).parents[5] / "prompts"

    @abstractmethod
    def format(self, **kwargs) -> Tuple[str, str]:
        pass
