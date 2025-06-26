from src.modules.nl_processor.prompts.base_prompt import BasePrompt
from src.modules.nl_processor.prompts.critic_prompt import CriticSinglePrompt, CriticFeedbackPrompt, CriticRepetitionPrompt

__all__ = [
    "BasePrompt",
    "CriticSinglePrompt",
    "CriticFeedbackPrompt",
    "CriticRepetitionPrompt",
]