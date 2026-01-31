# Hepsiburada NLP & Review Analysis (Airfryer Case Study)

Bu proje, Hepsiburada üzerindeki "Airfryer" (Fritöz) kategorisindeki en popüler ürünlere ait kullanıcı yorumlarını ve soru-cevap verilerini toplayarak; Doğal Dil İşleme (NLP), Duygu Analizi (Sentiment Analysis) ve TF-IDF yöntemleriyle tüketici içgörüleri çıkaran kapsamlı bir veri madenciliği ve strateji geliştirme çalışmasıdır.

## 📂 Proje Yapısı

Proje, verinin toplanmasından analiz edilmesine kadar modüler bir mimari ile kurgulanmıştır:

```text
hb-nlp/
├── data/
│   ├── processed/          # Temizlenmiş veriler, TF-IDF sonuçları ve WordCloud görselleri
│   └── raw/                # Scraper ile çekilen ham veriler (csv)
├── notebooks/              # EDA (Keşifçi Veri Analizi) ve Pattern denemeleri
├── src/
│   ├── analysis/           # NLP ve Analiz Motoru
│   │   ├── cleaner.py      # Metin temizliği ve ön işleme (Stopwords, Regex)
│   │   ├── tfidf_analyzer.py # TF-IDF algoritma modülü
│   │   ├── pattern_matcher.py # Kural tabanlı etiketleme
│   │   └── generate_wordcloud.py # Görselleştirme
│   ├── scraper/            # Veri Toplama Modülü
│   │   ├── scraper_comments.py
│   │   └── scraper_qna.py
│   └── main.py             # Ana çalıştırma dosyası
├── requirements.txt        # Gerekli kütüphaneler
└── README.md               # Proje dokümantasyonu
