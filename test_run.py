import os, requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY")

r = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {key}"}
)

print(r.status_code, r.text)