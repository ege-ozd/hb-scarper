import pandas as pd
import os
from src.analysis.cleaner import TurkishDataCleaner


def main():
    # 1. Ayarlar
    RAW_PATH = "/Users/tugberkozdemir/PycharmProjects/hb-nlp/data/raw/tum_yorumlar.csv"
    PROCESSED_PATH = "/Users/tugberkozdemir/PycharmProjects/hb-nlp/data/processed/tum_yorumlar_cleaned.csv"

    # 2. Veriyi Yükle
    print("Veri yükleniyor...")
    df = pd.read_csv(RAW_PATH, encoding='utf-16')

    # 3. Temizlik İşlemini Başlat
    cleaner = TurkishDataCleaner()

    # Varsayalım ki yorumlar sütununun adı 'yorum' veya 'comment'
    # Kendi CSV sütun adınla değiştir (Örn: 'content', 'text' vb.)
    target_column = 'yorum'  # Burayı CSV'ndeki başlığa göre güncelle!

    if target_column in df.columns:
        df = cleaner.apply_cleaning(df, target_column)

        # 4. Kaydet
        print(f"Temizlenmiş veri kaydediliyor: {PROCESSED_PATH}")
        df.to_csv(PROCESSED_PATH, index=False, encoding='utf-8-sig')  # Excel dostu kaydet
        print("İşlem başarıyla tamamlandı.")
    else:
        print(f"Hata: CSV içinde '{target_column}' sütunu bulunamadı!")
        print(f"Mevcut sütunlar: {df.columns.tolist()}")


if __name__ == "__main__":
    main()