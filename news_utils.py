import pandas as pd
from LAB_1.tokenizer import word_tokenizer

# ================================
# Load models
# ================================
unigram_df = pd.read_csv("LAB_4/Unigram_Model/unigram_model_laplace_smoothing.csv")   # word, count, prob
bigram_df = pd.read_csv("LAB_4/Bigram_Model/bigram_model_laplace_smoothing.csv")
trigram_df = pd.read_csv("LAB_4/Trigram_Model/trigram_model_laplace_smoothing.csv")
quadgram_df = pd.read_csv("LAB_4/Quadgram_Model/quadgram_model_laplace_smoothing.csv")

# ================================
# Convert to dicts for fast lookup
# ================================
unigram_counts = dict(zip(unigram_df["word"], unigram_df["count"]))
bigram_counts = dict(zip(zip(bigram_df["word1"], bigram_df["word2"]), bigram_df["count"]))
trigram_counts = dict(zip(zip(trigram_df["word1"], trigram_df["word2"], trigram_df["word3"]), trigram_df["count"]))
quadgram_counts = dict(zip(zip(quadgram_df["word1"], quadgram_df["word2"], quadgram_df["word3"], quadgram_df["word4"]), quadgram_df["count"]))

# Totals + vocab size
total_unigrams = sum(unigram_counts.values())
V = len(unigram_counts)
k = 1   # Laplace smoothing constant

# ================================
# Probability functions
# ================================
def unigram_prob(w):
    return (unigram_counts.get(w, 0) + k) / (total_unigrams + k * V)

def bigram_prob(w1, w2):
    count_bigram = bigram_counts.get((w1, w2), 0)
    count_unigram = unigram_counts.get(w1, 0)
    return (count_bigram + k) / (count_unigram + k * V)

def trigram_prob(w1, w2, w3):
    count_trigram = trigram_counts.get((w1, w2, w3), 0)
    count_bigram = bigram_counts.get((w1, w2), 0)
    return (count_trigram + k) / (count_bigram + k * V)

def quadgram_prob(w1, w2, w3, w4):
    count_quadgram = quadgram_counts.get((w1, w2, w3, w4), 0)
    count_trigram = trigram_counts.get((w1, w2, w3), 0)
    return (count_quadgram + k) / (count_trigram + k * V)

# ================================
# Sentence probability
# ================================
def sentence_probability(sentence, model="bigram"):
    words = ["<s>"] + word_tokenizer(sentence) + ["</s>"]
    prob = 1.0

    if model == "unigram":
        for w in words:
            prob *= unigram_prob(w)

    elif model == "bigram":
        for i in range(len(words)-1):
            prob *= bigram_prob(words[i], words[i+1])

    elif model == "trigram":
        for i in range(len(words)-2):
            prob *= trigram_prob(words[i], words[i+1], words[i+2])

    elif model == "quadgram":
        for i in range(len(words)-3):
            prob *= quadgram_prob(words[i], words[i+1], words[i+2], words[i+3])

    return prob
