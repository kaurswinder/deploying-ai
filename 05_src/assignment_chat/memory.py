"""
Memory management for conversation history with context window handling.
"""

from typing import List, Dict, Optional
from collections import deque


class ConversationMemory:
    """
    Manages conversation history with context window management.
    Implements a sliding window approach for long conversations.
    """
    
    def __init__(self, max_history_length: int = 10, token_limit: Optional[int] = None):
        """
        Initialize conversation memory.
        
        Args:
            max_history_length: Maximum number of message pairs to keep
            token_limit: Optional token limit for context (approximate)
        """
        self.max_history_length = max_history_length
        self.token_limit = token_limit
        self.messages: List[Dict[str, str]] = []
        self.system_message = ""
    

    def set_system_message(self, message: str):
        """Set the system message."""
        self.system_message = message
    
    def add_message(self, role: str, content: str):
        """
        Add a message to the conversation history.
        
        Args:
            role: "user" or "assistant"
            content: The message content
        """
        self.messages.append({
            "role": role,
            "content": content
        })
        
        # Trim history if exceeds max length
        self._trim_history()
    
    def _trim_history(self):
        """Trim conversation history based on max_history_length."""
        if len(self.messages) > self.max_history_length * 2:
            # Keep system context and recent messages
            # Remove older messages, but keep at least the most recent exchange
            num_to_remove = len(self.messages) - (self.max_history_length * 2)
            self.messages = self.messages[num_to_remove:]
    
    def get_conversation_for_model(self) -> List[Dict[str, str]]:
        """
        Get the conversation history formatted for the LLM.
        
        Returns:
            List of message dicts with 'role' and 'content'
        """
        return self.messages.copy()
    
    def get_summary(self) -> str:
        """Get a brief summary of the conversation so far."""
        if not self.messages:
            return "No conversation yet."
        
        user_messages = [m for m in self.messages if m["role"] == "user"]
        assistant_messages = [m for m in self.messages if m["role"] == "assistant"]
        
        return (
            f"Conversation stats: {len(user_messages)} user messages, "
            f"{len(assistant_messages)} assistant responses. "
            f"Current history length: {len(self.messages)} messages."
        )
    
    def clear_history(self):
        """Clear all conversation history."""
        self.messages = []
    
    def get_last_n_messages(self, n: int) -> List[Dict[str, str]]:
        """
        Get the last n messages.
        
        Args:
            n: Number of messages to retrieve
            
        Returns:
            List of last n messages
        """
        return self.messages[-n:] if self.messages else []
    
    def estimated_tokens(self) -> int:
        """
        Rough estimate of tokens in conversation.
        Uses ~4 characters per token as a heuristic.
        """
        total_chars = sum(len(m["content"]) for m in self.messages)
        return total_chars // 4


class MemoryManager:
    """
    Manages different types of memory for the chatbot.
    """
    
    def __init__(self):
        """Initialize the memory manager."""
        self.conversation = ConversationMemory(max_history_length=10)
        self.context_data = {}  # For storing any contextual information
    
    def start_new_conversation(self):
        """Start a new conversation."""
        self.conversation.clear_history()
        self.context_data = {}
    
    def get_memory_status(self) -> Dict[str, any]:
        """Get current status of all memory."""
        return {
            "conversation_length": len(self.conversation.messages),
            "estimated_tokens": self.conversation.estimated_tokens(),
            "summary": self.conversation.get_summary(),
        }
