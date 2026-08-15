from app.ai.schemas import TicketAnalysis
from app.core.config import settings
import requests

def ask_ai(prompt: str):

    response = requests.post(
        settings.OLLAMA_URL,
        json={
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    print("========== RESPUESTA OLLAMA ==========")
    print(data)
    print("======================================")

    return data["response"]