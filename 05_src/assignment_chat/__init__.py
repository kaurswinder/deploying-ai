"""
Assignment Chat - An AI conversational system with multiple services.
"""

from .engine import ChatEngine
from .interface import ChatInterface
from .services import APIService, SemanticSearchService, FunctionCallingService
from .memory import ConversationMemory, MemoryManager
from .guardrails import check_and_respond

__version__ = "1.0.0"

__all__ = [
    "ChatEngine",
    "ChatInterface",
    "APIService",
    "SemanticSearchService",
    "FunctionCallingService",
    "ConversationMemory",
    "MemoryManager",
    "check_and_respond",
]
