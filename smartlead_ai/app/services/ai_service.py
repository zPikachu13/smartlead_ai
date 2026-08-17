import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

BUSINESS_CONTEXT = os.getenv(
    "BUSINESS_CONTEXT",
    "Sen bir müşteri asistanısın. Müşterilerin sorularını nazik, profesyonel ve Türkçe olarak yanıtla. "
    "Müşteriyi iletişim bilgilerini bırakmaya teşvik et."
)


class AIService:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        # Groq üzerinde aktif olan güncel modeller listesi
        self.models = ["llama-3.1-8b-instant", "llama3-8b-8192", "gemma2-9b-it"]

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajına Groq API veya Fallback ile yanıt üretir."""
        
        # 1. API Anahtarı Kontrolü
        if not self.api_key:
            print("HATA: GROQ_API_KEY bulunamadı!")
            return "Merhaba! Sistem şu anda demo modunda çalışmaktadır. Sorunuz alındı, en kısa sürede dönüş yapacağız."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = [
            {"role": "system", "content": BUSINESS_CONTEXT}
        ]
        
        if gecmis and isinstance(gecmis, list):
            messages.extend(gecmis)
            
        messages.append({"role": "user", "content": mesaj})

        # Modelleri sırayla dener
        for model in self.models:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.3
            }

            try:
                response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=12)
                
                if response.status_code == 200:
                    result_json = response.json()
                    return result_json["choices"][0]["message"]["content"]
                else:
                    print(f"Groq API Hata ({model}): {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Bağlantı Hatası ({model}): {str(e)}")
                continue

        # Tüm modeller başarısız olursa devreye giren Fallback
        return "Talebinizi aldık. Uzman ekibimiz detaylı bilgi için sizinle iletişime geçecektir."


ai_service = AIService()