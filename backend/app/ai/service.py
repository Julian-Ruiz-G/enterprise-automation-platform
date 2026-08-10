from app.ai.schemas import TicketAnalysis
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"

def ask_ai(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
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