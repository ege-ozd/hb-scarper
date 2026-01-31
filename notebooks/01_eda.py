import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

from nltk import ngrams

# 1. Veriyi Yükle
df = pd.read_csv("/data/processed/tum_yorumlar_cleaned.csv")
text_data = df['cleaned_yorum'].dropna()

# 2. En Çok Geçen Kelimeler
all_words = " ".join(text_data).split()
word_freq = Counter(all_words)
common_words = pd.DataFrame(word_freq.most_common(20), columns=['Kelime', 'Frekans'])

print("\nEn Çok Geçen İlk 20 Kelime:")
print(common_words.head(20))

# 3. Görselleştirme
plt.figure(figsize=(12, 8))
sns.barplot(x='Frekans', y='Kelime', data=common_words, palette='viridis')
plt.title('En Çok Geçen 20 Kelime')
plt.show()

# 4. Yorum Uzunluğu Analizi
df['word_count'] = text_data.apply(lambda x: len(x.split()))
plt.figure(figsize=(10, 6))
sns.histplot(df['word_count'], bins=30, kde=True)

plt.title('Yorum Başına Kelime Sayısı Dağılımı')
plt.xlabel('Kelime Sayısı')
plt.ylabel('Yorum Sayısı')

max_wc = df['word_count'].max()
plt.xticks(np.arange(0, max_wc + 30, 30))
plt.show()


# 5. Bigram Hesaplama Fonksiyonu
def get_top_bigrams(corpus, n=2, top_k=20):
    all_words = " ".join(corpus).split()
    # NLTK'nın ngrams fonksiyonu ile ikilileri oluşturuyoruz
    bigram_list = list(ngrams(all_words, n))
    bigram_freq = Counter(bigram_list)
    return bigram_freq.most_common(top_k)

# 6. Analizi Çalıştır
top_20_bigrams = get_top_bigrams(text_data)

# Görselleştirme için DataFrame hazırla
# (('kargo', 'hizli'), 150) -> 'kargo hizli', 150
bigram_df = pd.DataFrame([
    {'Kelime Grubu': " ".join(item[0]), 'Frekans': item[1]}
    for item in top_20_bigrams
])

print("\n--- En Çok Geçen 20 Bigram ---")
print(bigram_df)

# 7. Görselleştirme
plt.figure(figsize=(12, 10))
sns.barplot(x='Frekans', y='Kelime Grubu', data=bigram_df, palette='rocket')
plt.title('En Sık Tekrar Eden İkili Kelime Grupları (Bigrams)')
plt.xlabel('Tekrar Sayısı')
plt.ylabel('Kalıplar (Patterns)')
plt.show()
