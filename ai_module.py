import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json"
}


def query(prompt):
    try:
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(API_URL, headers=HEADERS, json=data)

        if response.status_code != 200:
            return {"error": response.text}

        return response.json()

    except Exception as e:
        return {"error": str(e)}


# -------------------------
# SUMMARIZE
# -------------------------
def summarize(text):
    prompt = f"Summarize this text:\n{text[:1000]}"

    result = query(prompt)

    if "error" in result:
        return f"⚠️ Error:\n{result['error']}"

    return "📌 Summary:\n" + result["choices"][0]["message"]["content"]


# -------------------------
# QA
# -------------------------
def answer_question(context, question):
    prompt = f"""
Context:
{context[:1000]}

Question:
{question}
"""

    result = query(prompt)

    if "error" in result:
        return f"⚠️ Error:\n{result['error']}"

    return "💡 Answer:\n" + result["choices"][0]["message"]["content"]
