from app import create_app

# 3. Adımda yazdığımız fonksiyonu çağırıp uygulamamızı oluşturuyoruz
app = create_app()

# Sadece bu dosya doğrudan çalıştırıldığında sunucuyu başlat
if __name__ == "__main__":
    print("Sunucu baslatiliyor...")
    app.run(host="0.0.0.0", port=5000, debug=True)