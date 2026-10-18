"""
AI Client Engine (Gemini API Integration)
Enforces:
1. Anti-Prompt-Injection sanitization on all untrusted external content
2. Structured JSON response schemas
3. Graceful fallback when API key is not configured (never crashes)
"""

import os
import json
from typing import Dict, Any, Optional, List
import httpx

from config.settings import settings
from agents.base_agent import sanitize_untrusted_text


class AIClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = settings.gemini_model

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def generate_json_response(
        self,
        system_instruction: str,
        user_prompt: str,
        untrusted_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute an AI synthesis call with prompt injection defense.
        Returns parsed JSON dictionary.
        """
        sanitized_context = sanitize_untrusted_text(untrusted_context or "")
        combined_prompt = f"{user_prompt}\n\n### UNTRUSTED REFERENCE DATA (READ-ONLY):\n{sanitized_context}"

        if not self.is_configured():
            # Return deterministic fallback response structure
            return {
                "source": "AI_CLIENT_FALLBACK",
                "status": "API_KEY_NOT_CONFIGURED",
                "message": "Gemini API key is not configured. Configure GEMINI_API_KEY in Integration Settings for generative capabilities."
            }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": combined_prompt}]
                }
            ],
            "systemInstruction": {
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2
            }
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                res = client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        raw_text = candidates[0]["content"]["parts"][0]["text"]
                        return json.loads(raw_text)
                    return {"error": "Empty response from Gemini"}
                else:
                    return {
                        "error": f"Gemini API returned HTTP {res.status_code}",
                        "details": res.text
                    }
        except Exception as e:
            return {"error": f"Failed to contact Gemini API: {str(e)}"}


ai_client = AIClient()
