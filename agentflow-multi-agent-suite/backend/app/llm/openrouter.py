import httpx
import json
from typing import List, Dict, Any, Optional
from loguru import logger

from app.core.config import settings


DEFAULT_AGENT_MODELS = {
    "aria": ["deepseek/deepseek-chat-v3-0324:free", "moonshotai/kimi-k2:free", "google/gemini-2.5-flash-preview-05-20:free"],
    "scout": ["google/gemini-2.5-flash-preview-05-20:free", "deepseek/deepseek-chat-v3-0324:free"],
    "profiler": ["google/gemini-2.5-flash-preview-05-20:free", "deepseek/deepseek-chat-v3-0324:free"],
    "tailor": ["deepseek/deepseek-chat-v3-0324:free", "moonshotai/kimi-k2:free", "google/gemini-2.5-flash-preview-05-20:free"],
    "navigator": ["google/gemini-2.5-flash-preview-05-20:free", "deepseek/deepseek-chat-v3-0324:free"],
    "verifier": ["deepseek/deepseek-chat-v3-0324:free", "moonshotai/kimi-k2:free"],
    "executor": ["google/gemini-2.5-flash-preview-05-20:free", "deepseek/deepseek-chat-v3-0324:free"],
}


class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
            "Content-Type": "application/json",
        }

    async def chat_completion(self, messages: List[Dict[str, str]], model: Optional[str] = None, agent_id: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 1024, **kwargs) -> Dict[str, Any]:
        models_to_try = []
        if model:
            models_to_try = [model]
        elif agent_id and agent_id in DEFAULT_AGENT_MODELS:
            models_to_try = DEFAULT_AGENT_MODELS[agent_id]
        else:
            models_to_try = ["deepseek/deepseek-chat-v3-0324:free", "google/gemini-2.5-flash-preview-05-20:free"]

        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            for m in models_to_try:
                try:
                    payload["model"] = m
                    resp = await client.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        return {"ok": True, "model": m, "data": data}
                    else:
                        logger.warning(f"OpenRouter {m} failed: {resp.status_code} {resp.text[:200]}")
                except Exception as e:
                    logger.warning(f"OpenRouter {m} error: {e}")
            return {"ok": False, "error": "All models failed"}

    async def get_models(self):
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.get(f"{self.base_url}/models", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
        except Exception as e:
            logger.warning(f"Failed to fetch models: {e}")
        return {}


openrouter = OpenRouterClient()
