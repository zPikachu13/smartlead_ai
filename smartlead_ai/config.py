import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yükle
load_dotenv()


class Config:
  """Temel yapılandırma sınıfı."""

  SECRET_KEY = os.environ.get("SECRET_KEY", "varsayilan-guvensiz-anahtar")
  DATABASE_URL = os.environ.get("DATABASE_URL", "smartlead.db")

  # Groq Yapay Zekâ Ayarları
  GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
  AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

  # CORS Ayarları
  CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

  # Yapay Zekânın Kişiliği
  BUSINESS_CONTEXT = os.environ.get(
      "BUSINESS_CONTEXT",
      """Sen AdaPlant AI asistanısın. Ziyaretçilerin sorularını nazikçe, 
kısa ve profesyonel bir şekilde yanıtla. Kullanıcıları hizmetlerimiz hakkında 
bilgi almaya ve iletişim bilgilerini (isim, telefon vb.) bırakmaya teşvik et. Türkçe konuş.""",
  )


class DevelopmentConfig(Config):
  """Geliştirme ortamı ayarları."""

  DEBUG = True


class ProductionConfig(Config):
  """Canlı ortam (Render vb.) ayarları."""

  DEBUG = False


# Ortama göre uygun config nesnesini seçmek için sözlük
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}