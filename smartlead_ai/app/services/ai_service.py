import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Modül A: İşletmenizin kişiliği ve kuralları
BUSINESS_CONTEXT = os.getenv(
    "BUSINESS_CONTEXT",
    "Sen bir müşteri asistanısın. Müşterilerin sorularını nazik, profesyonel ve Türkçe olarak yanıtla. "
    "Müşteriyi iletişim bilgilerini bırakmaya teşvik et."
)


class AIServiceError(Exception):
    """Yapay zeka servisine özel hata sınıfı."""
    pass


class AIService:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = "llama-3.1-8b-instant"  

        # Yönergede belirtilen güncel model
    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajına Groq API veya Demo Modu ile yanıt üretir."""
        
        # 1. API Anahtarı Yoksa Demo Modu
        if not self.api_key:
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

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3
        }

        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                result_json = response.json()
                return result_json["choices"][0]["message"]["content"]
            else:
                # Groq geçici hata verirse devreye giren yedek (Demo)
                return "Talebinizi aldık. Uzman ekibimiz detaylı bilgi için sizinle iletişime geçecektir."

        except Exception:
            # Bağlantı kopsa dahi kullanıcıya kibar yanıt döner
            return "Şu anda sistemsel bir yoğunluk var. Lütfen formu doldurarak iletişim bilginizi bırakın."


# Tekil servis örneği
ai_service = AIService()