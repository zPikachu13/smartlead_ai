import os
import requests
from config import Config


class AIServiceError(Exception):
  """Yapay zekâ servisine özel hata sınıfı."""

  pass


class AIService:

  def __init__(self):
    self.api_key = Config.GROQ_API_KEY
    self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    self.model = "llama-3.1-8b-instant"

  def _sistem_talimati_al(self):
    """Config dosyasından işletme rolünü/kişiliğini döndürür."""
    return Config.BUSINESS_CONTEXT

  def yanit_uret(self, mesaj, gecmis=None):
    """Kullanıcı mesajını ve varsa önceki geçmişi alıp Groq API'den yanıt döndürür."""

    if not self.api_key or self.api_key.strip() == "":
      return "Demo Modu: Groq API anahtarı bulunamadı. Lütfen .env dosyanızı kontrol edin."

    if gecmis is None:
      gecmis = []

    # Mesaj listesini hazırla
    messages = [{"role": "system", "content": self._sistem_talimati_al()}]

    # Varsa önceki sohbet geçmişini ekle
    for g in gecmis:
      messages.append(g)

    # En son kullanıcı mesajını ekle
    messages.append({"role": "user", "content": mesaj})

    headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": self.model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500,
    }

    try:
      response = requests.post(
          self.api_url, headers=headers, json=payload, timeout=15
      )

      # HTTP durum kodu 200 değilse hata
      if response.status_code != 200:
        raise AIServiceError(
            f"Groq API Hatası (Kod {response.status_code}): {response.text}"
        )

      data = response.json()
      ai_cevabi = data["choices"][0]["message"]["content"]
      return ai_cevabi

    except requests.exceptions.RequestException as e:
      raise AIServiceError(f"Bağlantı hatası oluştu: {str(e)}")


# Diğer dosyalarda doğrudan kullanılacak tekil servis örneği
ai_service = AIService()