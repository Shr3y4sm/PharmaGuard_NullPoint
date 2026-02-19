import os
import json
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_clinical_recommendation(self, prompt: str) -> dict:
        """Generate clinical recommendation from prompt."""
        pass


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider."""
    
    def __init__(self, api_key: str = None):
        """Initialize Gemini provider.
        
        Parameters:
        -----------
        api_key : str
            Google API key (if None, will look for GOOGLE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not provided or set in environment")
        
        self.model = "gemini-2.5-flash"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def generate_clinical_recommendation(self, prompt: str) -> dict:
        """
        Generate clinical recommendation using Google Gemini.
        
        Parameters:
        -----------
        prompt : str
            The prompt for the LLM
            
        Returns:
        --------
        dict
            Structured response with clinical_recommendation and llm_generated_explanation
        """
        try:
            import requests
            
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract text from response
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    text = candidate["content"]["parts"][0]["text"]
                    
                    # Try to parse as JSON
                    try:
                        # First try direct JSON parsing
                        parsed_response = json.loads(text)
                        return parsed_response
                    except json.JSONDecodeError:
                        # Try to extract JSON from markdown code blocks
                        try:
                            import re
                            # Look for JSON in code blocks (```json ... ```)
                            json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
                            if json_match:
                                json_text = json_match.group(1)
                                parsed_response = json.loads(json_text)
                                return parsed_response
                        except:
                            pass
                        
                        # If still can't parse, structure it
                        return {
                            "clinical_recommendation": {
                                "dosage_adjustment": text[:200] if len(text) > 200 else text,
                                "monitoring": "Refer to clinical guidelines"
                            },
                            "llm_generated_explanation": {
                                "summary": text
                            }
                        }
            
            return self._default_response()
        
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._default_response()
    
    def _default_response(self) -> dict:
        """Return default response if API call fails."""
        return {
            "clinical_recommendation": {
                "dosage_adjustment": "Consult healthcare provider",
                "monitoring": "Standard monitoring recommended"
            },
            "llm_generated_explanation": {
                "summary": "Unable to generate LLM explanation at this time"
            }
        }


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def __init__(self, api_key: str = None):
        """Initialize OpenAI provider.
        
        Parameters:
        -----------
        api_key : str
            OpenAI API key (if None, will look for OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not provided or set in environment")
        
        self.model = "gpt-4"
        self.base_url = "https://api.openai.com/v1"
    
    def generate_clinical_recommendation(self, prompt: str) -> dict:
        """
        Generate clinical recommendation using OpenAI.
        
        Parameters:
        -----------
        prompt : str
            The prompt for the LLM
            
        Returns:
        --------
        dict
            Structured response with clinical_recommendation and llm_generated_explanation
        """
        try:
            import requests
            
            url = f"{self.base_url}/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                choice = result["choices"][0]
                if "message" in choice:
                    text = choice["message"]["content"]
                    
                    # Try to parse as JSON
                    try:
                        parsed_response = json.loads(text)
                        return parsed_response
                    except json.JSONDecodeError:
                        # If not JSON, structure it
                        return {
                            "clinical_recommendation": {
                                "dosage_adjustment": text[:200],
                                "monitoring": "Refer to clinical guidelines"
                            },
                            "llm_generated_explanation": {
                                "summary": text
                            }
                        }
            
            return self._default_response()
        
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._default_response()
    
    def _default_response(self) -> dict:
        """Return default response if API call fails."""
        return {
            "clinical_recommendation": {
                "dosage_adjustment": "Consult healthcare provider",
                "monitoring": "Standard monitoring recommended"
            },
            "llm_generated_explanation": {
                "summary": "Unable to generate LLM explanation at this time"
            }
        }


def get_llm_provider(provider_name: str = "gemini", api_key: str = None) -> LLMProvider:
    """
    Factory function to get an LLM provider instance.
    
    Parameters:
    -----------
    provider_name : str
        Name of the provider ("gemini" or "openai")
    api_key : str
        API key for the provider
        
    Returns:
    --------
    LLMProvider
        Instance of the specified provider
    """
    provider_name = provider_name.lower()
    
    if provider_name == "gemini":
        return GeminiProvider(api_key)
    elif provider_name == "openai":
        return OpenAIProvider(api_key)
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
