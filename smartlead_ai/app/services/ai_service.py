import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Groq istemcisini başlat
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def analyze_lead(text):
    """Müşteri metnini Groq ile analiz eder ve sözlük olarak döner."""
    system_prompt = (
        "Sen bir müşteri analiz uzmanısın. Yanıtını JSON formatında ver. "
        "Alanlar: score (1-100), urgency (Düşük/Orta/Yüksek), summary (özet), reply (yanıt)."
    )
    user_prompt = f"Mesajı analiz et: {text}"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        # Gelen JSON metnini Python sözlüğüne (dict) çeviriyoruz
        raw_result = response.choices[0].message.content
        data = json.loads(raw_result)
        return {"success": True, "data": data}

    except Exception as e:
        return {"success": False, "error": str(e)}