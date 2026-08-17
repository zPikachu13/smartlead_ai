import uuid
from flask import Blueprint, request, jsonify
from app.services.ai_service import ai_service

api_bp = Blueprint("api", __name__)
leads_db = []


@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "API basariyla calisiyor."}), 200


@api_bp.route("/sohbet", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "mesaj" not in data:
        return jsonify({"basari": False, "error": "Mesaj alani zorunludur."}), 400

    mesaj = data["mesaj"].strip()
    if not mesaj:
        return jsonify({"basari": False, "error": "Mesaj bos olamaz."}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj)
        return jsonify({"basari": True, "yanit": cevap, "cevap": cevap}), 200
    except Exception as e:
        return jsonify({"basari": False, "error": "AI servisine ulasilamadi."}), 503


@api_bp.route("/leads", methods=["GET", "POST"])
def manage_leads():
    if request.method == "POST":
        data = request.get_json()
        if not data or "isim" not in data or "telefon" not in data:
            return jsonify({"basari": False, "error": "İsim ve telefon zorunludur."}), 400

        new_lead = {
            "_id": str(uuid.uuid4()),
            "isim": data.get("isim"),
            "telefon": data.get("telefon"),
            "email": data.get("email", ""),
            "mesaj": data.get("mesaj", "")
        }
        leads_db.append(new_lead)
        return jsonify({"basari": True, "data": new_lead}), 201

    return jsonify({"basari": True, "data": leads_db}), 200