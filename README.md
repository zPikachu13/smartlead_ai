# 🌿 AdaPlant AI - Akıllı Müşteri Asistanı ve Lead Yönetim Sistemi

Bu proje, işletmeler için gelen müşteri sorularını yapay zekâ destekli (Groq LLM) olarak canlı yanıtlayan, potansiyel müşteri (lead) bilgilerini toplayan ve bu kayıtları işletme sahibinin yönetebileceği bir yönetim panelinde (B2B Dashboard) listeleyen uçtan uca bir mikroservis mimarisidir.

---

## 🚀 Canlı Bağlantılar

- **Canlı Backend (Render):** `https://adaplant-ai.onrender.com`
- **Canlı Frontend (Wix):** `https://adayigitdemirtas.wixstudio.com/adaplant`

---

## 🛠️ Mimari ve Teknolojiler

Proje **Sorumlulukların Ayrılığı (Separation of Concerns - SoC)** ilkesine uygun olarak katmanlı mimaride inşa edilmiştir:

* **Backend / API:** Python (Flask), Flask-CORS, Gunicorn
* **Yapay Zekâ Entegrasyonu:** Groq Cloud API (`llama-3.1-8b-instant`, `openai/gpt-oss-20b`) + Akıllı Fallback / Demo Modu
* **Bulut Dağıtımı (Deployment):** Render Web Service
* **Frontend:** Wix Studio & Wix Velo (JavaScript - `wix-fetch`, `wix-location-frontend`)
* **Veri Yönetimi:** RESTful JSON API

---

## 📂 Proje Dizin Yapısı

```text
adaplant-ai/
├── app/
│   ├── services/
│   │   └── ai_service.py       # Yapay zekâ ve fallback servis katmanı
│   ├── routes.py               # REST API uç noktaları (/health, /sohbet, /leads)
│   └── __init__.py             # Flask Blueprint ve CORS yapılandırması
├── .env.example                # Örnek çevre değişkenleri
├── .gitignore                  # Git hariç tutma dosyası (.env vb.)
├── requirements.txt            # Python bağımlılıkları
├── run.py                      # Uygulama başlatıcı
└── README.md                   # Proje dokümantasyonu
