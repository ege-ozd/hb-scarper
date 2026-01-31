import pandas as pd
import os
from src.analysis.pattern_matcher import AirfryerPatternMatcher

def run_insight_analysis():
    input_path = "/Users/tugberkozdemir/PycharmProjects/hb-nlp/data/processed/tum_yorumlar_cleaned.csv"
    output_path = "/Users/tugberkozdemir/PycharmProjects/hb-nlp/data/processed/tum_yorumlar_with_insights.csv"

    if not os.path.exists(input_path):
        print("Hata: Veri bulunamadı!")
        return

    df = pd.read_csv(input_path)
    matcher = AirfryerPatternMatcher()

    print("Kalıplar 'puan' desteği ile analiz ediliyor...")

    # DİKKAT: Burada puan sütununu da matcher'a gönderiyoruz
    df['insight_category'] = df.apply(
        lambda row: matcher.cluster_by_pattern(row['cleaned_yorum'], row['puan']),
        axis=1
    )

    # Bağlam analizini kontrol için tutalım (Şimdilik tüm gri kelimeler için)
    gri_list = ["gerek yok", "ürün çok", "daha iyi", "daha önce"]
    def get_all_contexts(text):
        contexts = []
        for target in gri_list:
            ctx = matcher.get_context(text, target, window=5)
            if ctx: contexts.append(f"[{target.upper()}]: {ctx}")
        return " | ".join(contexts) if contexts else None

    df['patterns_context'] = df['cleaned_yorum'].apply(get_all_contexts)

    df.to_csv(output_path, index=False)
    print("\n" + "="*30 + "\nANALİZ ÖZETİ\n" + "="*30)
    # Birden fazla etiket olabileceği için value_counts biraz karışabilir ama temel dağılımı verir
    print(df['insight_category'].str.split(' | ').explode().value_counts())
    print("="*30)

if __name__ == "__main__":
    run_insight_analysis()