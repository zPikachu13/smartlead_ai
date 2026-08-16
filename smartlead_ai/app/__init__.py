from flask import Flask, jsonify
from flask_cors import CORS
from app.routes import api_bp


def create_app():
    """Flask uygulamasını başlatan ve ayarlarını yapan temel fonksiyon."""
    app = Flask(__name__)
    
    # Wix ve dış kaynaklardan gelen isteklere izin veriyoruz
    CORS(app)

    # 2. Adımda oluşturduğumuz rotaları /api ön ekiyle bağlıyoruz
    app.register_blueprint(api_bp, url_prefix="/api")

    # Duman Testi 
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "status": "online",
            "service": "SmartLead AI",
            "message": "Uygulama basariyla calisiyor."
        }), 200

    return app