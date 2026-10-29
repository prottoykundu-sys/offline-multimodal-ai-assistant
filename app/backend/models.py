import os
import requests
import json

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

class LocalModelClient:
    def __init__(self, base_url=OLLAMA_URL):
        self.base_url = base_url

    def list_models(self):
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=20)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e), "models": []}

    def generate(self, model: str, prompt: str, system: str = None, stream: bool = False):
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        if system:
            payload["system"] = system

        r = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()

    def chat(self, model: str, messages: list, stream: bool = False):
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        r = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()
