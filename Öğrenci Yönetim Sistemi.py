# 1. Öğrenci verileri için sözlük
ogrenciler = {}

# 2. Yeni öğrenci ekleme fonksiyonu
def ogrenci_ekle():
    numara = input("Öğrenci numarasını girin: ")
    isim = input("Öğrenci adını girin: ")
    
    # 3. Hata yakalama ile not alma
    while True:
        try:
            not_bilgisi = float(input("Öğrenci notunu girin: "))
            break
        except:
            print("Sadece sayı girin")

    # Sözlüğe ekleme
    ogrenciler[numara] = {
        "isim": isim,
        "not": not_bilgisi
    }
    print("Öğrenci eklendi")


# 4. Sonsuz döngü (while True)
while True:
    print("\n--- MENÜ ---")
    print("1 - Öğrenci Ekle")
    print("2 - Öğrencileri Listele")
    print("3 - Çıkış")
    
    secim = input("Seçiminiz: ")

    # 5. if-elif-else ile menü kontrolü
    if secim == "1":
        ogrenci_ekle()
        
    elif secim == "2":
        print("\n--- ÖĞRENCİ LİSTESİ ---")
        for numara in ogrenciler:
            print("Numara:", numara, "İsim:", ogrenciler[numara]["isim"], "Not:", ogrenciler[numara]["not"])
            
    elif secim == "3":
        print("Görüşürüz")
        break
        
    else:
        print("Yanlış seçim yaptınız")