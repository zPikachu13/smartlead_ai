import uuid
from flask import Blueprint, request, jsonify
from app.services.ai_service import analyze_lead

api_bp = Blueprint("api", __name__)

# Lead verilerini saklamak için geçici liste
leads_db = []


@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "API basariyla calisiyor."}), 200


# 1. Sohbet Rotası (B2C Karşılama Sayfası için)
@api_bp.route("/sohbet", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "mesaj" not in data:
        return jsonify({"success": False, "error": "Mesaj alani zorunludur."}), 400

    user_message = data["mesaj"].strip()
    if not user_message:
        return jsonify({"success": False, "error": "Mesaj bos olamaz."}), 400

    result = analyze_lead(user_message)
    if not result["success"]:
        return jsonify({"success": False, "error": result["error"]}), 500

    return jsonify({
        "success": True,
        "yanit": result["data"].get("reply", "Mesajiniz analiz edildi."),
        "detay": result["data"]
    }), 200


# 2. Leads Rotası (POST: Kaydet, GET: Panelde Listele)
@api_bp.route("/leads", methods=["GET", "POST"])
def manage_leads():
    if request.method == "POST":
        data = request.get_json()
        if not data or "isim" not in data or "telefon" not in data:
            return jsonify({"success": False, "error": "İsim ve telefon alanlari zorunludur."}), 400

        # Wix Repeater için benzersiz _id alanı eklenir
        new_lead = {
            "_id": str(uuid.uuid4()),
            "isim": data.get("isim"),
            "telefon": data.get("telefon"),
            "mesaj": data.get("mesaj", ""),
            "durum": "Yeni"
        }
        leads_db.append(new_lead)
        return jsonify({"success": True, "data": new_lead}), 201

    # GET isteği: Tüm lead'leri listeler
    return jsonify({"success": True, "data": leads_db}), 200