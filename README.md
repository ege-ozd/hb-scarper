# Hepsiburada NLP & Review Analysis (Airfryer Case Study)

Bu proje, Hepsiburada üzerindeki "Airfryer" (Fritöz) kategorisindeki en popüler ürünlere ait kullanıcı yorumlarını ve soru-cevap verilerini toplayarak; Doğal Dil İşleme (NLP), Duygu Analizi (Sentiment Analysis) ve TF-IDF yöntemleriyle tüketici içgörüleri çıkaran kapsamlı bir veri madenciliği çalışmasıdır.

## 📂 Proje Yapısı

```text
hb-nlp/
├── data/
│   ├── processed/          # İşlenmiş ve analize hazır veriler (TF-IDF çıktıları, temizlenmiş CSV'ler)
│   └── raw/                # Scraper ile çekilen ham veriler (yorumlar, soru-cevaplar)
├── notebooks/              # EDA ve Pattern analizleri için Jupyter/Python notebookları
├── src/
│   ├── analysis/           # NLP, Temizlik ve Analiz modülleri
│   │   ├── cleaner.py      # Veri temizliği ve ön işleme
│   │   ├── tfidf_analyzer.py # TF-IDF algoritması
│   │   └── ...
│   ├── scraper/            # Hepsiburada veri kazıma botları
│   └── main.py             # Ana çalıştırma dosyası
├── requirements.txt        # Gerekli kütüphaneler
└── README.md               # Proje dokümantasyonu