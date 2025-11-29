"""
Offline LLM Provider for CrewAI.
Provides a fallback mechanism using a CSV-based knowledge base when no API keys are available.
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

class OfflineLLM:
    """
    A Mock LLM that responds based on a CSV knowledge base.
    Implements the interface expected by CrewAI/LiteLLM for text generation.
    """
    
    def __init__(self, knowledge_base_path: str = None):
        self.knowledge_base_path = knowledge_base_path or str(Path(__file__).parent / "data" / "offline_responses.csv")
        self.responses = self._load_knowledge_base()
        self.model_name = "offline-fallback-model"

    def _load_knowledge_base(self) -> List[Dict[str, str]]:
        """Load the CSV data into memory."""
        if not os.path.exists(self.knowledge_base_path):
            print(f"⚠️ Warning: Offline knowledge base not found at {self.knowledge_base_path}")
            return []
            
        loaded_data = []
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Parse keywords into a list for easier matching
                    row['keyword_list'] = [k.strip().lower() for k in row.get('keywords', '').split(',')]
                    loaded_data.append(row)
        except Exception as e:
            print(f"❌ Error loading offline knowledge base: {e}")
            
        return loaded_data

    def _find_best_match(self, prompt: str) -> str:
        """Find the best response from the knowledge base based on prompt keywords."""
        prompt_lower = prompt.lower()
        best_match = None
        max_score = 0
        
        for entry in self.responses:
            # Calculate a simple score based on keyword matching
            score = 0
            for keyword in entry['keyword_list']:
                if keyword in prompt_lower:
                    score += 1
            
            # Context boosting: if the prompt mentions the specific swarm type, boost it
            if entry.get('swarm') in prompt_lower:
                score += 2
                
            if score > max_score:
                max_score = score
                best_match = entry
        
        if best_match and max_score > 0:
            return best_match['response']
        
        return self._get_generic_fallback(prompt)

    def _get_generic_fallback(self, prompt: str) -> str:
        """Return a generic response if no specific match is found."""
        return (
            "**[OFFLINE MODE]**\n\n"
            "I am operating in offline mode without an LLM API key. "
            "I received your request but couldn't find a specific pre-canned response for it in my database.\n\n"
            f"**Your Prompt was:** \"{prompt[:100]}...\"\n\n"
            "To see specific offline responses, try keywords like 'eda', 'training', 'market analysis', or 'architecture'."
        )

    def call(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Simulate an LLM call. 
        Accepts standard messages list format: [{'role': 'user', 'content': '...'}]
        """
        # Extract the last user message
        user_message = ""
        if isinstance(messages, list):
            for msg in reversed(messages):
                if msg.get('role') == 'user':
                    user_message = msg.get('content', '')
                    break
        elif isinstance(messages, str):
            user_message = messages
            
        return self._find_best_match(user_message)

    # Compatibility methods for CrewAI/LiteLLM expectations
    def chat(self, messages, **kwargs):
        """Alias for call to match some interface expectations."""
        class MockResponse:
            def __init__(self, content):
                self.content = content
                self.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': content})})]
        
        response_text = self.call(messages)
        return MockResponse(response_text)
        
    def __call__(self, *args, **kwargs):
        """Allow the instance to be called directly."""
        # Handle different calling conventions
        if args:
            return self.call(args[0])
        if 'messages' in kwargs:
            return self.call(kwargs['messages'])
        return self._get_generic_fallback("")


