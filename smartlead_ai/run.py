import os
from app import create_app

# Ortam değişkenine göre uygulamayı başlat
env = os.environ.get("FLASK_ENV", "default")
app = create_app(env)

if __name__ == "__main__":
  # Yerel geliştirme için 5000 portunda başlat
  app.run(host="0.0.0.0", port=5000, debug=True)