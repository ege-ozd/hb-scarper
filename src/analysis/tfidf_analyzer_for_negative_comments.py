import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# --- HARDCODED TURKISH STOPWORDS ---
# These are words we want to IGNORE because they don't carry specific meaning
TR_STOPWORDS = [
    'acaba', 'ama', 'aslında',  'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz',
    'bu', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem',
    'hep', 'hepsi', 'her', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu',
    'mü', 'nasıl', 'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o',
    'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya', 'yani', 'bir', 'kadar',
    'olarak', 'ben', 'sen', 'onlar', 'bunu', 'bunun', 'buna', 'bile',
    'falan', 'filan', 'ancak', 'lakin', 'fakat', 'oysa', 'kendi', 'kendine', 'zaten',
    'olsa', 'olsun', 'oldu', 'olan', 'olduğu', 'bence', 'tam', 'bile'
    # --- DOMAIN SPECIFIC NOISE ---
    'ürün', 'ürünü', 'aldım', 'geldi', 'ulaştı', 'elime', 'hepsiburada', 'teşekkürler',
    'teşekkür', 'ederim', 'tavsiye', 'ediyorum'
]

# 2. Phrase Blocklist (Exact phrases from your result list to remove)
# These are the ones that slipped through the single-word filter or are specific combos.
PHRASE_BLOCKLIST = [
    'çok güzel', 'gayet güzel', 'çok iyi', 'güzel ürün', 'çok memnun',
    'memnun kaldım', 'çok memnunum', 'çok beğendim', 'harika ürün', 'ürün güzel',
    'iyi almışım', 'gayet iyi', 'çok başarılı', 'ürün çok güzel',
    'memnun kaldık', 'tercih ettim', 'gayet yeterli', 'cok guzel', 'çok memnunuz',
    'güzel çok', 'cok iyi', 'çok ideal', 'bi ürün', 'çok memnun kaldık',
    'güzel kaliteli', 'güzel beğendim', 'ürün sağlam', 'sorunsuz geldi',
    'ürün mükemmel', 'uzun araştırmalar', 'güzel tavsiye', 'güzel yapıyor',
    'çok güzel çok', 'yapmak istedim', 'yorum yapmak istedim', 'gelir gelmez', 'gerçekten çok',
    'gayet başarılı', 'çok memnun kaldım', 'ertesi gün', 'çok fazla',
    'onun dışında', 'hak ediyor', 'çok beğendik', 'çok çok', ' ürün çok', 'ürün gayet',
    'ürün gayet güzel', 'kullandıktan sonra', 'mükemmel ürün', 'yaptım çok',
    'air fryer', 'çok beğendi', 'denedim çok'


]

def run_tfidf_analysis(input_path, output_path, top_n=50):
    """
    Loads cleaned reviews, performs TF-IDF, calculates global importance scores
    for terms, and saves the results.
    """
    # 1. Load Data
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)

    # Ensure cleaned_yorum is string and drop NaNs
    df['cleaned_yorum'] = df['cleaned_yorum'].astype(str)
    df = df[df['cleaned_yorum'].notna()]
    df = df[df['cleaned_yorum'] != 'nan']  # Handle string 'nan' if present

    print(f"Analyzing {len(df)} reviews...")

    # 2. Initialize Vectorizer
    # ngram_range=(1, 2,): Captures unigrams ('airfryer') and bigrams ('hızlı pişiriyor')
    # min_df=0.01: Ignores terms that appear in less than 1% of reviews (removes outliers)
    # max_df=0.95: Ignores terms that appear in more than 95% of reviews (removes generic words)
    tfidf = TfidfVectorizer(
        ngram_range=(1, 3),
        min_df=10,  # Ignore terms appearing in fewer than 10 reviews
        max_df=0.90,  # Ignore terms appearing in > 90% of reviews
        max_features = 10000,  # Limit to top 10k features to keep analysis sharp
        stop_words=TR_STOPWORDS
    )

    # 3. Fit and Transform
    # This creates a matrix of shape (n_reviews, n_unique_terms)
    tfidf_matrix = tfidf.fit_transform(df['cleaned_yorum'])
    feature_names = tfidf.get_feature_names_out()

    print(f"Vocabulary size: {len(feature_names)} unique terms.")

    # 4. Aggregate Scores (Global Importance)
    # We calculate the mean TF-IDF score for each column (term)
    # Note: We convert to array because tfidf_matrix is a sparse matrix
    print("Calculating mean scores...")
    mean_scores = np.array(tfidf_matrix.mean(axis=0)).flatten()

    # Create a DataFrame for the terms and their scores
    tfidf_df = pd.DataFrame({
        'term': feature_names,
        'tfidf_score': mean_scores
    })

    # --- FILTERING STEP ---
    # Remove terms that match our Blocklist exactly
    print(f"Filtering out {len(PHRASE_BLOCKLIST)} specific phrases...")
    tfidf_df = tfidf_df[~tfidf_df['term'].isin(PHRASE_BLOCKLIST)]

    # 5. Sort from Most Valuable to Least
    tfidf_df = tfidf_df.sort_values(by='tfidf_score', ascending=False)

    # Save detailed results
    tfidf_df.to_csv(output_path, index=False)
    print(f"TF-IDF analysis saved to {output_path}")

    # Display Top N
    print(f"\n--- Top {top_n} Most Valuable Terms ---")
    print(tfidf_df.head(top_n).to_string(index=False))


if __name__ == "__main__":
    # Define paths based on your project structure

    INPUT_FILE = "/data/processed/tum_yorumlar_1_2_3_puan.csv"
    OUTPUT_FILE = "/data/processed/tfidf_1_2_3_puan.csv"

    run_tfidf_analysis(INPUT_FILE, OUTPUT_FILE)
