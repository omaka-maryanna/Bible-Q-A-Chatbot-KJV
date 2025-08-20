import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found. Please add it to your .env file.")

def ask_groq(prompt: str) -> str:
    """
    Sends a prompt to the Groq API and returns the AI's response.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",   # Fast + accurate model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # raises HTTPError for bad codes
    except requests.exceptions.RequestException as e:
        raise Exception(f"⚠️ Groq API request failed: {e}")

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise Exception(f"⚠️ Unexpected Groq API response format: {response.text}")