"""
Guardrails module for restricting topics and protecting system prompts.
"""

import re
from typing import Tuple

# Restricted topics that the chatbot should not engage with
RESTRICTED_TOPICS = {
    "cats": ["cat", "cats", "feline", "kitten", "kitty", "meow"],
    "dogs": ["dog", "dogs", "canine", "puppy", "pup", "woof", "doggo"],
    "horoscopes": ["horoscope", "horoscopes", "zodiac", "zodiac sign", "astrology", "astrological"],
    "taylor swift": ["taylor swift", "taylor", "swift", "folklore", "reputation", "eras tour"],
}

SYSTEM_PROMPT_KEYWORDS = [
    "system prompt",
    "system message",
    "you are",
    "you're",
    "your instructions",
    "your directive",
    "your role",
    "my instructions",
    "my directive",
    "my role",
    "what are you",
    "who are you",
    "tell me about yourself",
    "describe yourself",
    "what is your purpose",
    "your purpose",
]


def is_restricted_topic(user_input: str) -> Tuple[bool, str]:
    """
    Check if user input contains restricted topics.
    
    Args:
        user_input: The user's input message
        
    Returns:
        Tuple of (is_restricted, topic_name)
    """
    user_input_lower = user_input.lower()
    
    for topic, keywords in RESTRICTED_TOPICS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', user_input_lower):
                return True, topic
    
    return False, ""


def is_system_prompt_attack(user_input: str) -> bool:
    """
    Check if user is trying to access or modify system prompt.
    
    Args:
        user_input: The user's input message
        
    Returns:
        True if attack detected, False otherwise
    """
    user_input_lower = user_input.lower()
    
    for keyword in SYSTEM_PROMPT_KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', user_input_lower):
            return True
    
    return False


def get_restricted_topic_response(topic: str) -> str:
    """
    Get a response for restricted topics.
    
    Args:
        topic: The restricted topic name
        
    Returns:
        An appropriate response message
    """
    responses = {
        "cats": "I appreciate your interest, but I'm not able to discuss cats. Is there something else I can help you with?",
        "dogs": "I'd love to chat about dogs, but that's actually a topic I have to avoid. What else can I help you with?",
        "horoscopes": "Horoscopes and astrology aren't my area - I don't discuss zodiac signs or astrological predictions. Want to talk about something else?",
        "taylor swift": "I can't discuss Taylor Swift or her work. Is there another topic you'd like to explore?",
    }
    
    return responses.get(topic, "I'm not able to discuss that topic. Can we talk about something else?")


def check_and_respond(user_input: str) -> Tuple[bool, str]:
    """
    Comprehensive check for restricted content and system prompt attacks.
    
    Args:
        user_input: The user's input message
        
    Returns:
        Tuple of (should_proceed, response_if_blocked)
    """
    # Check for system prompt attacks
    if is_system_prompt_attack(user_input):
        return False, "I can't discuss my internal instructions or system prompts. How can I help you with something else?"
    
    # Check for restricted topics
    is_restricted, topic = is_restricted_topic(user_input)
    if is_restricted:
        return False, get_restricted_topic_response(topic)
    
    return True, ""
