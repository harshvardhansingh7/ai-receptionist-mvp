import requests
from app.config import GROQ_API_KEY

def call_llm(messages):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "openai/gpt-oss-120b",
            "messages": messages
        }

        response = requests.post(url, headers=headers, json=body)

        data = response.json()

        if "choices" not in data:
            print("ERROR RESPONSE:", data)
            return "Sorry, AI is having trouble right now."

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("LLM ERROR:", e)
        return "Something went wrong."