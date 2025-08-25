import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found. Please add it to your .env file.")

def ask_groq(prompt: str, retries: int = 3, delay: int = 2) -> str:
    """
    Sends a prompt to the Groq API and returns the AI's response.
    Retries automatically if Groq fails temporarily.
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

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()  # raises HTTPError for bad codes

            # Parse and return AI response
            return response.json()["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            # Retry if not the last attempt
            if attempt < retries:
                time.sleep(delay * attempt)  # exponential backoff
            else:
                # On final failure, show Groq's actual error
                try:
                    error_details = response.json()
                except Exception:
                    error_details = str(e)
                raise Exception(
                    f"⚠️ Groq API request failed after {retries} attempts.\n👉 Details: {error_details}"
                )

        except (KeyError, IndexError):
            raise Exception(f"⚠️ Unexpected Groq API response format: {response.text}")