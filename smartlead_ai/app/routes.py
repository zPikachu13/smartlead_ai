from flask import Blueprint, request, jsonify
from app.services.ai_service import analyze_lead

# Blueprint tanımı (Web rotalarını toplayan temel yapı)
api_bp = Blueprint("api", __name__)


# 1. Duman Testi
@api_bp.route("/health", methods=["GET"])
def health_check():
    """Sunucunun ve servisin ayakta olduğunu gösteren basit kontrol."""
    return jsonify({
        "status": "healthy",
        "message": "API basariyla calisiyor."
    }), 200


# 2. Ana Analiz Rotası
@api_bp.route("/analyze", methods=["POST"])
def analyze():
    """Wix'ten gelen metni alır, doğrular ve AI sonucunu döner."""
    
    # Gelen JSON verisini sözlük olarak alıyoruz
    data = request.get_json()

    # Girdi Doğrulama
    if not data or "text" not in data:
        return jsonify({
            "success": False,
            "error": "Lutfen 'text' alanini doldurun."
        }), 400

    user_text = data["text"].strip()
    if user_text == "":
        return jsonify({
            "success": False,
            "error": "Metin alani bos birakilamaz."
        }), 400

    # 1. Adımda yazdığımız ai_service fonksiyonunu çağırıyoruz
    result = analyze_lead(user_text)

    # Sonucu kontrol edip istemciye iletiyoruz
    if not result["success"]:
        return jsonify({
            "success": False,
            "error": result["error"]
        }), 500

    return jsonify({
        "success": True,
        "data": result["data"]
    }), 200