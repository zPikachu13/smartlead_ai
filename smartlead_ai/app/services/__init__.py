from config import config_by_name
from flask import Flask, jsonify
from flask_cors import CORS


def create_app(config_name="default"):
  """Flask Uygulama Fabrikası (Application Factory)"""
  app = Flask(__name__)

  # 1. Ayarları yükle
  app.config.from_object(config_by_name[config_name])

  # 2. CORS'u aktifleştir (Frontend bağlantısı için)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  # 3. Veritabanını ilklendir (Tablolar yoksa oluştur)
  from app.database import init_db

  with app.app_context():
    init_db()

  # 4. Blueprint'leri (Rotaları) kaydet
  from app.routes import api_bp, main_bp

  app.register_blueprint(main_bp)
  app.register_blueprint(api_bp, url_prefix="/api")

  # 5. Canlılık (Health Check) Uç Noktası
  @app.route("/health")
  def health_check():
    return (
        jsonify({
            "durum": "aktif",
            "servis": "SmartLead AI (AdaPlant)",
            "versiyon": "1.0.0",
        }),
        200,
    )

  return app