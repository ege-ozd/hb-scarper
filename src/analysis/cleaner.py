import re
import pandas as pd


class TurkishDataCleaner:
    def __init__(self):
        # Stopword listesi
        self.stopwords = ["ve", "bir", "bu", "da", "de", "için", "en", "mi", "mı", "mu", "ki", "ise", "ile", "gibi", "o", "şu", "ben", "biz", "siz", "onlar"]

    def turkish_lower(self, text):
        
        if not isinstance(text, str): return ""
        
        mapping = {"İ": "i", "I": "ı", "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç"}
        for key, value in mapping.items():
            text = text.replace(key, value)
        return text.lower()

    def clean_text(self, text):
        if not isinstance(text, str) or text.strip() == "":
            return ""

        # 1. Küçük harf dönüşümü
        text = self.turkish_lower(text)

        # 2. URL, E-posta ve Sayıları temizleme
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'\d+', '', text)  # Sayıları da temizliyoruz (istatistiği bozmasın)

        # 3. Özel karakterleri ve Emojileri temizleme
        text = re.sub(r'[^a-zıığüşöç\s]', ' ', text)

        # 4. Fazla boşlukları temizleme
        text = re.sub(r'\s+', ' ', text).strip()

        # 5. Stopword Temizliği
        text = " ".join([word for word in text.split() if word not in self.stopwords])

        return text

    def apply_cleaning(self, df, column_name):
        print(f"--- {column_name} sütunu temizleniyor ---")
        # .astype(str) ekleyerek boş (NaN) satırların hata vermesini engelliyoruz
        df[f'cleaned_{column_name}'] = df[column_name].astype(str).apply(self.clean_text)
        return df
