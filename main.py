from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

app = FastAPI()

DEESEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEESEEK_URL = "https://api.deepseek.com/chat/completions"

if not DEESEEK_API_KEY:
    raise RuntimeError("Please set the DEEPSEEK_API_KEY environment variable.")

class Question(BaseModel):
    prompt: str

@app.post("/ask")
def ask(question: Question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEESEEK_API_KEY}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question.prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(DEESEEK_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error calling DeepSeek API: {e}")

    result = response.json()
    # DeepSeek عادةً يعيد الرسالة تحت result["choices"][0]["message"]["content"]
    try:
        answer = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Unexpected response format from DeepSeek API.")

    return {"answer": answer}
