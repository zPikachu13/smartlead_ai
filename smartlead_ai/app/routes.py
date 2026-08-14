from flask import Blueprint, jsonify, render_template, request
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service

# 1. Blueprint: Web sayfaları için
main_bp = Blueprint("main", __name__)

# 2. Blueprint: JSON API servisleri için
api_bp = Blueprint("api", __name__)


# -------------------------------------------------------------
# Sayfa Rotaları (HTML)
# -------------------------------------------------------------
@main_bp.route("/")
def index():
  """Ziyaretçi Karşılama Sayfası (B2C)"""
  return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
  """Yönetim Paneli Sayfası (B2B)"""
  return render_template("dashboard.html")


# -------------------------------------------------------------
# API Uç Noktaları (JSON)
# -------------------------------------------------------------
@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
  """Yapay zekâ ile mesajlaşma uç noktası."""
  veri = request.get_json()

  if not veri or "mesaj" not in veri or not veri["mesaj"].strip():
    return (
        jsonify({"basari": False, "hata": "Lütfen bir mesaj metni gönderin."}),
        400,
    )

  mesaj = veri["mesaj"].strip()
  gecmis = veri.get("gecmis", [])

  try:
    cevap = ai_service.yanit_uret(mesaj=mesaj, gecmis=gecmis)
    return jsonify({"basari": True, "cevap": cevap}), 200
  except AIServiceError as e:
    return (
        jsonify({
            "basari": False,
            "hata": "Yapay zekâ servisine şu anda ulaşılamıyor.",
            "detay": str(e),
        }),
        503,
    )
  except Exception as e:
    return (
        jsonify({
            "basari": False,
            "hata": "Beklenmeyen bir sunucu hatası oluştu.",
        }),
        500,
    )


@api_bp.route("/leads", methods=["POST"])
def yeni_lead():
  """Yeni müşteri adayı kaydetme uç noktası."""
  veri = request.get_json()

  if not veri:
    return (
        jsonify({"basari": False, "hata": "Geçersiz veri formatı (JSON yok)."}),
        400,
    )

  isim = veri.get("isim", "").strip()
  telefon = veri.get("telefon", "").strip()
  mesaj = veri.get("mesaj", "").strip()

  # Zorunlu alan kontrolü
  if not isim or not telefon:
    return (
        jsonify(
            {"basari": False, "hata": "İsim ve telefon alanları zorunludur."}
        ),
        400,
    )

  try:
    yeni_id = lead_ekle(isim=isim, telefon=telefon, mesaj=mesaj)
    return (
        jsonify({
            "basari": True,
            "mesaj": "Kayıt başarıyla oluşturuldu.",
            "lead_id": yeni_id,
        }),
        201,
    )
  except Exception as e:
    return (
        jsonify({"basari": False, "hata": "Veritabanı kayıt hatası oluştu."}),
        500,
    )


@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():
  """Tüm kayıtları listeleme uç noktası."""
  try:
    kayitlar = tum_leadler()
    return (
        jsonify({
            "basari": True,
            "toplam": len(kayitlar),
            "leadler": kayitlar,
        }),
        200,
    )
  except Exception as e:
    return (
        jsonify(
            {"basari": False, "hata": "Kayıtlar getirilirken hata oluştu."}
        ),
        500,
    )