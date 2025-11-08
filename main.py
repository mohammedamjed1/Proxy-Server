from fastapi import FastAPI, Request
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# للسماح لبابل بالاتصال
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكنك تحديد رابط تطبيق Bubble فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEESEEK_API_KEY = "sk-14807e0a014546759cb630b50e5e3663"
DEESEEK_URL = "https://api.deepseek.ai/v1/generate"

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    payload = {
        "prompt": prompt,
        "max_tokens": 500
    }
    headers = {"Authorization": f"Bearer {DEESEEK_API_KEY}"}
    response = requests.post(DEESEEK_URL, json=payload, headers=headers)
    return response.json()
