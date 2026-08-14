import os
import sqlite3
from config import Config

DB_PATH = Config.DATABASE_URL


def get_db():
  """Veritabanı bağlantısı açar ve satırlara sütun adıyla erişim sağlar."""
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn


def init_db(app=None):
  """'leads' tablosunu oluşturur (eğer daha önce oluşturulmadıysa)."""
  conn = get_db()
  cursor = conn.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


def lead_ekle(isim, telefon, mesaj=""):
  """Yeni bir potansiyel müşteri (lead) kaydeder.

  SQL Injection'a karşı '?' yer tutucusu kullanır.
  """
  conn = get_db()
  cursor = conn.cursor()

  cursor.execute(
      """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
    """,
      (isim, telefon, mesaj),
  )

  conn.commit()
  yeni_id = cursor.lastrowid
  conn.close()
  return yeni_id


def tum_leadler():
  """Tüm kayıtları en yeniden eskiye doğru liste sözlükleri olarak döndürür."""
  conn = get_db()
  cursor = conn.cursor()

  cursor.execute("""
        SELECT id, isim, telefon, mesaj, tarih 
        FROM leads 
        ORDER BY tarih DESC
    """)
  rows = cursor.fetchall()
  conn.close()

  lead_listesi = []
  for row in rows:
    lead_listesi.append({
        "id": row["id"],
        "isim": row["isim"],
        "telefon": row["telefon"],
        "mesaj": row["mesaj"],
        "tarih": row["tarih"],
    })

  return lead_listesi