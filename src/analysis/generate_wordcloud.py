import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os


def generate_tfidf_wordcloud(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)

    # Convert the dataframe into a dictionary: { 'term': score }
    
    weights = dict(zip(df['term'], df['tfidf_score']))

    print("Generating Word Cloud...")

    # Initialize WordCloud
    
    wc = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        font_path='/System/Library/Fonts/Supplemental/Arial.ttf',
        colormap='viridis',  # 'plasma', 'inferno', 'viridis' are good options
        max_words=100
    )

    
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
    INPUT_FILE = "/data/processed/tfidf_keywords.csv"
    OUTPUT_IMAGE = "/data/processed/tfidf_wordcloud.png"

    generate_tfidf_wordcloud(INPUT_FILE, OUTPUT_IMAGE)
