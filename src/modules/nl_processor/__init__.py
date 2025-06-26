# src/llm/__init__.py

"""
LLM Package

This package provides tools to manage an LLM server instance (LLMServerManager)
and to communicate with it via API calls (LLMAPIClient).

Modules:
    server_manager: Contains the LLMServerManager class for starting/stopping/checking the server.
    client: Contains the LLMAPIClient class for performing HTTP API requests.
"""

from .llm_client import LLMClient
from .local_llm_client import LocalLLMClient
from .gemini_client import GeminiClient
from .llm_server_manager import LLMServerManager

__all__ = [
    "LLMServerManager",
    "LLMClient",
    "LocalLLMClient",
    "GeminiClient",
]