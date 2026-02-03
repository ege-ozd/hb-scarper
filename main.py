import pandas as pd
import os
from src.analysis.cleaner import TurkishDataCleaner


def main():
    # 1. Ayarlar
    RAW_PATH = "/data/raw/tum_yorumlar.csv"
    PROCESSED_PATH = "/data/processed/tum_yorumlar_cleaned.csv"

    # 2. Veriyi Yükle
    print("Veri yükleniyor...")
    df = pd.read_csv(RAW_PATH, encoding='utf-16')

    # 3. Temizlik İşlemini Başlat
    cleaner = TurkishDataCleaner()

    
    target_column = 'yorum'  

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
