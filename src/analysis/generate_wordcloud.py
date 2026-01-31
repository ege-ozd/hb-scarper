import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os


def generate_tfidf_wordcloud(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)

    # Convert the dataframe into a dictionary: { 'term': score }
    # This tells the wordcloud exactly how big to draw each word
    weights = dict(zip(df['term'], df['tfidf_score']))

    print("Generating Word Cloud...")

    # Initialize WordCloud
    # font_path: We point to Arial on Mac to ensure Turkish characters (ş, ı, ğ) render correctly.
    # If this path doesn't exist, remove the 'font_path' argument.
    wc = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        font_path='/System/Library/Fonts/Supplemental/Arial.ttf',
        colormap='viridis',  # 'plasma', 'inferno', 'viridis' are good options
        max_words=100
    )

    # key step: generate from the frequencies we calculated
    wc.generate_from_frequencies(weights)

    # Show the plot
    plt.figure(figsize=(20, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')  # Hide the x/y axis numbers

    # Save to file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Word Cloud saved to {output_path}")

    # Optional: Show it on screen if you run this in a setting that supports UI
    # plt.show()


if __name__ == "__main__":
    # Define paths
    INPUT_FILE = "/Users/tugberkozdemir/PycharmProjects/hb-nlp/data/processed/tfidf_keywords.csv"
    OUTPUT_IMAGE = "/Users/tugberkozdemir/PycharmProjects/hb-nlp/data/processed/tfidf_wordcloud.png"

    generate_tfidf_wordcloud(INPUT_FILE, OUTPUT_IMAGE)