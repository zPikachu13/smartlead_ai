import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def analyze_lead(text):
    """Müşteri metnini Groq API ile analiz eder."""
    if not GROQ_API_KEY:
        return {"success": False, "error": "GROQ_API_KEY bulunamadi."}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "Sen bir musteri analiz ve destek uzmanisin. Yanitini JSON formatinda ver. "
        "Alanlar: score (1-100 arasi puan), urgency (Dusuk/Orta/Yuksek), summary (kisa ozet), reply (musteriye verilecek nazik ve aciklayici yanit)."
    )

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Mesaji analiz et ve yanitla: {text}"}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=20)
        
        if response.status_code != 200:
            return {"success": False, "error": f"Groq Hatasi: {response.text}"}

        result_json = response.json()
        raw_content = result_json["choices"][0]["message"]["content"]
        data = json.loads(raw_content)
        
        return {"success": True, "data": data}

    except Exception as e:
        return {"success": False, "error": str(e)}