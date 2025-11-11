"""
Main chat engine that orchestrates services, memory, and guardrails.
"""

import os
from typing import Optional, Tuple, List, Dict
from openai import OpenAI

from .services import APIService, SemanticSearchService, FunctionCallingService
from .memory import MemoryManager
from .guardrails import check_and_respond


class ChatEngine:
    """
    Main orchestrator for the conversational AI system.
    Integrates services, memory management, and guardrails.
    """
    
    def __init__(self, api_key: Optional[str] = None, chroma_db_path: str = "./chroma_db"):
        """
        Initialize the chat engine.
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            chroma_db_path: Path for ChromaDB persistent storage
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and OPENAI_API_KEY env var not set")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Initialize services
        self.api_service = APIService()
        self.semantic_service = SemanticSearchService(chroma_db_path)
        self.function_service = FunctionCallingService()
        
        # Initialize memory
        self.memory = MemoryManager()
        
        # Set system prompt with personality
        self.system_prompt = """You are Aria, a knowledgeable and friendly AI assistant with a curious, engaging personality. 
You have a helpful demeanor and enjoy learning about various topics. You're resourceful and can:

1. Answer questions by searching a knowledge base
2. Provide weather information for locations
3. Help with calculations and word definitions
4. Maintain natural, flowing conversations

When a user asks about weather, acknowledge it and mention you can help with that.
When they ask questions that might benefit from your knowledge base, search it.
When they ask for calculations or definitions, use your function calling abilities.

Be warm, conversational, and always maintain a respectful tone. If something is outside your capabilities or restricted, 
politely explain why you can't help with that particular topic and offer an alternative way to assist."""
    
    def process_message(self, user_input: str) -> Tuple[str, Dict[str, any]]:
        """
        Process a user message and generate a response.
        
        Args:
            user_input: The user's message
            
        Returns:
            Tuple of (response_text, metadata_dict)
        """
        metadata = {
            "guardrails_triggered": False,
            "restricted_topic": None,
            "services_used": [],
        }
        
        # Check guardrails
        should_proceed, blocked_response = check_and_respond(user_input)
        if not should_proceed:
            metadata["guardrails_triggered"] = True
            if "system prompt" in blocked_response.lower():
                metadata["restricted_topic"] = "system_prompt"
            else:
                metadata["restricted_topic"] = "restricted_topic"
            return blocked_response, metadata
        
        # Add user message to memory
        self.memory.conversation.add_message("user", user_input)
        
        # Determine which services to use based on user input
        should_search = self._should_semantic_search(user_input)
        should_get_weather = self._should_get_weather(user_input)
        should_calculate = self._should_calculate(user_input)
        
        # Gather context from services
        service_context = ""
        
        if should_search:
            search_results = self.semantic_service.search(user_input, num_results=2)
            if search_results:
                service_context += "\nRelevant knowledge base results:\n"
                for result in search_results:
                    service_context += f"- {result['text'][:200]}...\n"
                metadata["services_used"].append("semantic_search")
        
        if should_get_weather:
            # Simple weather for Toronto as example
            weather_info = self.api_service.get_weather(43.6532, -79.3832, "Toronto")
            service_context += f"\nWeather Information: {weather_info}\n"
            metadata["services_used"].append("api_weather")
        
        if should_calculate:
            # Try to extract and calculate
            calc_result = self._attempt_calculation(user_input)
            if calc_result:
                service_context += f"\nCalculation: {calc_result}\n"
                metadata["services_used"].append("calculator")
        
        # Build messages for LLM
        messages = [
            {"role": "system", "content": self.system_prompt + service_context}
        ]
        
        # Add conversation history
        messages.extend(self.memory.conversation.get_conversation_for_model())
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to memory
            self.memory.conversation.add_message("assistant", assistant_message)
            
            metadata["memory_status"] = self.memory.get_memory_status()
            
            return assistant_message, metadata
            
        except Exception as e:
            error_message = f"I encountered an error processing your request: {str(e)}"
            return error_message, metadata
    
    def _should_semantic_search(self, user_input: str) -> bool:
        """Determine if semantic search should be performed."""
        search_triggers = [
            "what is", "tell me about", "explain", "how", "why",
            "what are", "describe", "information about", "know about"
        ]
        user_lower = user_input.lower()
        return any(trigger in user_lower for trigger in search_triggers)
    
    def _should_get_weather(self, user_input: str) -> bool:
        """Determine if weather information should be retrieved."""
        weather_triggers = [
            "weather", "temperature", "rain", "snow", "sunny", "cloudy",
            "forecast", "conditions", "climate", "wind", "humidity"
        ]
        user_lower = user_input.lower()
        return any(trigger in user_lower for trigger in weather_triggers)
    
    def _should_calculate(self, user_input: str) -> bool:
        """Determine if calculation should be attempted."""
        calc_triggers = [
            "calculate", "math", "compute", "what is", "how much",
            "+", "-", "*", "/", "times", "divided", "plus", "minus"
        ]
        user_lower = user_input.lower()
        return any(trigger in user_lower for trigger in calc_triggers)
    
    def _attempt_calculation(self, user_input: str) -> Optional[str]:
        """Try to extract and calculate from user input."""
        # Look for simple mathematical expressions
        import re
        # Find patterns like "2 + 3", "5 * 4", etc.
        pattern = r'(\d+[\+\-\*/]\d+)'
        match = re.search(pattern, user_input)
        if match:
            expression = match.group(1)
            return self.function_service.call_function("calculator", expr=expression)
        return None
    
    def reset_conversation(self):
        """Start a new conversation."""
        self.memory.start_new_conversation()
    
    def get_available_functions(self) -> Dict[str, str]:
        """Get descriptions of available functions."""
        return self.function_service.get_available_functions()
