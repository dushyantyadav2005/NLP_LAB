import re
import matplotlib.pyplot as plt
from tqdm import tqdm

# --- Helper Functions from Assignment 1 ---
# These are included to make the script self-contained if needed,
# but the main logic reads from the pre-tokenized file.

def sentence_tokenizer(paragraph):
    """Splits a Hindi paragraph into sentences."""
    pattern = r'[\u0964!?.][^0-9\u0966-\u096F]'
    sentences = re.split(pattern, paragraph)
    ends = re.findall(pattern, paragraph)
    res = []
    for sentence in sentences:
        if not ends:
            break
        end = ends.pop(0)
        res.append(sentence.strip() + end)
    return res if res else [paragraph]

def word_tokenizer(sentence):
    """Splits a Hindi sentence into words and other tokens."""
    url_pattern = r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(?:\+?[0-9\u0966-\u096F]{1,3}[\s-]?)?[0-9\u0966-\u096F]{10}'
    time_pattern = r'[0-9\u0966-\u096F]{1,2}:[0-9\u0966-\u096F]{2}'
    latin_number = r'[0-9]+(?:\.[0-9]+)?'
    devnag_number = r'[\u0966-\u096F]+(?:\.[\u0966-\u096F]+)?'
    punctuation = r'[!?\.\u0964\,"\'\+-]'
    hindi_word = r'[\u0900-\u0963\u0965-\u097F]+'
    english_word = r'[a-zA-Z]+'
    emoji_pattern = r'[\U0001F300-\U0001FAFF\U00002700-\U000027BF]'
    pattern = fr'{email_pattern}|{url_pattern}|{phone_pattern}|{time_pattern}|{latin_number}|{devnag_number}|{punctuation}|{hindi_word}|{emoji_pattern}|{english_word}'
    return re.findall(pattern, sentence)

# --- Core Logic for Frequency Analysis ---

def create_frequency_distribution(file_path):
    """
    Reads a tokenized file and creates a frequency distribution of words.
    Args:
        file_path (str): The path to the tokenized text file.
    Returns:
        dict: A dictionary with words as keys and their frequencies as values.
    """
    freq_dist = {}
    print(f"Reading from {file_path} to create frequency distribution...")
    with open(file_path, "r", encoding="utf-8") as fin:
        for line in tqdm(fin, desc="Processing lines"):
            tokens = line.strip().split()
            for token in tokens:
                # Increment the count for the token
                freq_dist[token] = freq_dist.get(token, 0) + 1
    return freq_dist

def plot_top_words(freq_dist, title, num_words=100):
    """
    Plots the most frequent words from a frequency distribution.
    Args:
        freq_dist (dict): The frequency distribution dictionary.
        title (str): The title for the plot.
        num_words (int): The number of top words to plot.
    """
    # Sort the dictionary by frequency in descending order
    sorted_words = sorted(freq_dist.items(), key=lambda item: item[1], reverse=True)
    
    # Get the top N words and their frequencies
    top_words = [item[0] for item in sorted_words[:num_words]]
    top_frequencies = [item[1] for item in sorted_words[:num_words]]

    # --- Plotting Configuration ---
    # To display Hindi characters correctly, you may need a font that supports Devanagari.
    # Examples: 'Nirmala UI' on Windows, 'Devanagari MT' on Mac, 'Lohit Devanagari' on Linux.
    # If you get squares instead of characters, try a different font.
    try:
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Nirmala UI'] # Change this to a font on your system
    except:
        print("Warning: Could not set a specific font for Hindi. Characters may not render correctly.")
        print("Please install a Devanagari-supporting font like 'Nirmala UI' or 'Lohit Devanagari'.")

    plt.figure(figsize=(20, 10))
    plt.bar(top_words, top_frequencies)
    plt.xlabel("Words (Tokens)")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.xticks(rotation=90)
    plt.tight_layout() # Adjust layout to make room for rotated labels
    plt.show()

def remove_stop_words(freq_dist, threshold):
    """
    Removes words from a frequency distribution based on a frequency threshold.
    Args:
        freq_dist (dict): The original frequency distribution.
        threshold (int): Any word with a frequency HIGHER than this will be removed.
    Returns:
        dict: A new frequency distribution without the stop words.
    """
    stop_words = {word for word, freq in freq_dist.items() if freq > threshold}
    print(f"\nIdentified {len(stop_words)} stop words with frequency > {threshold}.")
    
    # Create a new dictionary excluding the stop words
    filtered_dist = {word: freq for word, freq in freq_dist.items() if word not in stop_words}
    return filtered_dist

# --- Main Execution ---

if __name__ == "__main__":
    input_file = "tokenized_hindi.txt"

    # 1. Create the initial frequency distribution
    full_freq_dist = create_frequency_distribution(input_file)

    # 2. Plot the most frequent 100 words before stop word removal
    plot_top_words(full_freq_dist, "Top 100 Most Frequent Words (Before Stop Word Removal)")

    # 3. Define thresholds and plot after removing stop words for each
    thresholds = [500, 1000, 1500] # You can change these values

    for threshold in thresholds:
        # Remove stop words based on the current threshold
        filtered_distribution = remove_stop_words(full_freq_dist, threshold)
        
        # Plot the top 100 remaining words
        plot_title = f"Top 100 Words (After Removing Stop Words with Freq > {threshold})"
        plot_top_words(filtered_distribution, plot_title)
