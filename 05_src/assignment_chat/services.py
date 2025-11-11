"""
Three services: API calls, semantic search, and function calling.
"""

import json
import requests
import chromadb
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class APIService:
    """
    Service 1: API Calls Service
    Uses the Open-Meteo Weather API to get weather data and transforms it naturally.
    """
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        """Initialize the API service."""
        pass
    
    def get_weather(self, latitude: float, longitude: float, city_name: str) -> str:
        """
        Get weather information for a location using Open-Meteo API and transform it.
        
        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            city_name: Name of the city for natural response
            
        Returns:
            Natural language description of the weather
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,weather_code,relative_humidity_2m,wind_speed_10m",
                "temperature_unit": "celsius"
            }
            
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            current = data["current"]
            temp = current["temperature_2m"]
            humidity = current["relative_humidity_2m"]
            wind_speed = current["wind_speed_10m"]
            weather_code = current["weather_code"]
            
            # Transform weather code to description
            weather_desc = self._get_weather_description(weather_code)
            
            # Create a natural language response
            response_text = (
                f"Here's the weather in {city_name}: It's currently {temp}°C with {weather_desc}. "
                f"The humidity is at {humidity}% and winds are blowing at {wind_speed} km/h. "
                f"It's a great day to stay informed about the conditions around you!"
            )
            
            return response_text
            
        except requests.RequestException as e:
            return f"I couldn't fetch the weather data at the moment. Please try again later. Error: {str(e)}"
    
    def _get_weather_description(self, code: int) -> str:
        """Map weather code to natural description."""
        descriptions = {
            0: "clear skies",
            1: "mostly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy conditions",
            48: "foggy conditions with frost",
            51: "light drizzle",
            61: "light rain",
            63: "moderate rain",
            65: "heavy rain",
            71: "light snow",
            73: "moderate snow",
            75: "heavy snow",
            77: "snow grains",
            80: "light rain showers",
            81: "moderate rain showers",
            82: "violent rain showers",
            85: "light snow showers",
            86: "heavy snow showers",
            95: "thunderstorm conditions",
            96: "thunderstorm with light hail",
            99: "thunderstorm with heavy hail",
        }
        return descriptions.get(code, "variable conditions")


class SemanticSearchService:
    """
    Service 2: Semantic Query Service
    Uses ChromaDB with persistent storage for semantic search over documents.
    """
    
    def __init__(self, chroma_db_path: str = "./chroma_db"):
        """Initialize the semantic search service with persistent ChromaDB."""
        self.db_path = Path(chroma_db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Create persistent client
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample documents if collection is empty."""
        if self.collection.count() == 0:
            sample_docs = [
                {
                    "id": "doc_1",
                    "text": "The Great Wall of China is one of the most impressive architectural feats in human history. "
                            "Built over many centuries, it spans approximately 13,000 miles across northern China.",
                    "metadata": {"topic": "history", "region": "Asia"}
                },
                {
                    "id": "doc_2",
                    "text": "Python is a high-level programming language known for its simplicity and readability. "
                            "It's widely used in data science, web development, and artificial intelligence.",
                    "metadata": {"topic": "technology", "subject": "programming"}
                },
                {
                    "id": "doc_3",
                    "text": "Climate change refers to long-term shifts in global temperatures and weather patterns. "
                            "It's primarily driven by human activities that increase greenhouse gas emissions.",
                    "metadata": {"topic": "environment", "subject": "climate"}
                },
                {
                    "id": "doc_4",
                    "text": "Machine learning is a subset of artificial intelligence that enables systems to learn from data. "
                            "It powers modern applications like recommendation systems, autonomous vehicles, and medical diagnostics.",
                    "metadata": {"topic": "technology", "subject": "AI"}
                },
                {
                    "id": "doc_5",
                    "text": "The Renaissance was a cultural movement spanning the 14th to 17th centuries that marked the transition "
                            "from medieval to modern Europe, bringing advances in art, science, and philosophy.",
                    "metadata": {"topic": "history", "period": "Renaissance"}
                },
            ]
            
            for doc in sample_docs:
                self.collection.add(
                    ids=[doc["id"]],
                    documents=[doc["text"]],
                    metadatas=[doc["metadata"]]
                )
    
    def search(self, query: str, num_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search the knowledge base semantically.
        
        Args:
            query: The search query
            num_results: Number of results to return
            
        Returns:
            List of results with documents and metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=num_results
            )
            
            formatted_results = []
            if results["documents"] and len(results["documents"]) > 0:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "text": doc,
                        "distance": results["distances"][0][i] if results["distances"] else 0,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                    })
            
            return formatted_results
        except Exception as e:
            return []
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Add new documents to the knowledge base.
        
        Args:
            documents: List of dicts with 'id', 'text', and optional 'metadata'
        """
        for i, doc in enumerate(documents):
            doc_id = doc.get("id", f"doc_{i}_{datetime.now().timestamp()}")
            self.collection.add(
                ids=[doc_id],
                documents=[doc["text"]],
                metadatas=[doc.get("metadata", {})]
            )


class FunctionCallingService:
    """
    Service 3: Function Calling Service
    Provides function calling capabilities for tool use.
    """
    
    def __init__(self):
        """Initialize the function calling service."""
        self.tools = {
            "calculator": self._calculate,
            "time_info": self._get_time_info,
            "define_word": self._define_word,
        }
    
    def _calculate(self, expression: str) -> str:
        """Simple calculator function."""
        try:
            # Only allow safe math operations
            import math
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"I couldn't calculate that. Please make sure the expression is valid. Error: {str(e)}"
    
    def _get_time_info(self) -> str:
        """Get current time information."""
        now = datetime.now()
        return (
            f"Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}. "
            f"It's currently {now.strftime('%H:%M')} in UTC+0 timezone."
        )
    
    def _define_word(self, word: str) -> str:
        """Provide simple word definitions."""
        definitions = {
            "serendipity": "The occurrence of events by chance in a happy or beneficial way",
            "ephemeral": "Lasting for a very short time",
            "ubiquitous": "Present, appearing, or found everywhere",
            "eloquent": "Fluent, persuasive, and expressive in speaking or writing",
            "pragmatic": "Dealing with things in a practical, realistic way based on actual circumstances",
        }
        
        word_lower = word.lower()
        if word_lower in definitions:
            return f"**{word}**: {definitions[word_lower]}"
        else:
            return f"I don't have a definition for '{word}' in my database. Try asking about another word!"
    
    def call_function(self, function_name: str, **kwargs) -> str:
        """
        Call a function by name with arguments.
        
        Args:
            function_name: Name of the function to call
            **kwargs: Arguments for the function
            
        Returns:
            Result of the function call
        """
        if function_name not in self.tools:
            return f"Function '{function_name}' is not available. Available functions: {', '.join(self.tools.keys())}"
        
        try:
            func = self.tools[function_name]
            if function_name == "time_info":
                return func()
            else:
                # For other functions, pass the first argument
                arg = list(kwargs.values())[0] if kwargs else ""
                return func(arg)
        except Exception as e:
            return f"Error calling function: {str(e)}"
    
    def get_available_functions(self) -> Dict[str, str]:
        """Get descriptions of available functions."""
        return {
            "calculator": "Evaluate a mathematical expression (e.g., '2 + 2 * 3')",
            "time_info": "Get current date and time information",
            "define_word": "Get the definition of a word",
        }
