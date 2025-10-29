import pandas as pd
from collections import defaultdict

# =========================
# Paths
# =========================
tokenized_file = "LAB_1/tokenized_hindi.txt"
bigram_csv = "LAB_4/Bigram_Model/bigram_model_laplace_smoothing.csv"  # or your saved bigram counts file
output_laplace = "LAB_4/Trigram_Model/trigram_model_laplace.csv"
output_k = "LAB_4/Trigram_Model/trigram_model_k_smoothing.csv"

# =========================
# Load Precomputed Bigrams
# =========================
bigram_df = pd.read_csv(bigram_csv, encoding="utf-8")

# Dictionary for bigram counts
bigram_counts = defaultdict(int)
for _, row in bigram_df.iterrows():
    w1, w2, count = row["word1"], row["word2"], int(row["count"])
    bigram_counts[(w1, w2)] = count

# =========================
# Count Unigrams + Trigrams
# =========================
unigram_counts = defaultdict(int)
trigram_counts = defaultdict(int)

max_lines = 100000  # <-- process only first 100,000 lines

with open(tokenized_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= max_lines:
            break

        words = line.strip().split()
        words = ["<s>"] + words + ["</s>"]  # add sentence boundaries

        # unigrams
        for w in words:
            unigram_counts[w] += 1

        # trigrams
        for j in range(len(words) - 2):
            trigram = (words[j], words[j+1], words[j+2])
            trigram_counts[trigram] += 1

# =========================
# Compute Probabilities
# =========================
k = [1, 10]  # Laplace and K-smoothing
V = len(unigram_counts)  # vocabulary size

trigram_model_lap = []
trigram_model_k = []

for (w1, w2, w3), count in trigram_counts.items():
    bigram_count = bigram_counts.get((w1, w2), 0)  # denominator

    # Laplace smoothing (k=1)
    prob_lap = (count + k[0]) / (bigram_count + V * k[0])

    # General k-smoothing (k=10)
    prob_k = (count + k[1]) / (bigram_count + V * k[1])

    trigram_model_lap.append([w1, w2, w3, count, prob_lap])
    trigram_model_k.append([w1, w2, w3, count, prob_k])

# =========================
# Save Models
# =========================
trigram_df_lap = pd.DataFrame(trigram_model_lap, columns=["word1", "word2", "word3", "count", "prob"])
trigram_df_k = pd.DataFrame(trigram_model_k, columns=["word1", "word2", "word3", "count", "prob"])

trigram_df_lap.to_csv(output_laplace, index=False, encoding="utf-8")
trigram_df_k.to_csv(output_k, index=False, encoding="utf-8")

print("✅ Trigram models saved (first 100,000 lines only).")
