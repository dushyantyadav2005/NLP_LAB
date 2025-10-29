import pandas as pd
from collections import defaultdict

# =========================
# Paths
# =========================
tokenized_file = "LAB_1/tokenized_hindi.txt"
trigram_csv = "LAB_4/Trigram_Model/trigram_model_laplace.csv"  # precomputed trigram counts file
output_laplace = "LAB_4/Quadgram_Model/quadgram_model_laplace.csv"
output_k = "LAB_4/Quadgram_Model/quadgram_model_k_smoothing.csv"

# =========================
# Load Precomputed Trigrams
# =========================
trigram_df = pd.read_csv(trigram_csv, encoding="utf-8")

# Dictionary for trigram counts
trigram_counts = defaultdict(int)
for _, row in trigram_df.iterrows():
    w1, w2, w3, count = row["word1"], row["word2"], row["word3"], int(row["count"])
    trigram_counts[(w1, w2, w3)] = count

# =========================
# Count Unigrams + Quadgrams
# =========================
unigram_counts = defaultdict(int)
quadgram_counts = defaultdict(int)

max_lines = 100000  # process only first 100,000 lines

with open(tokenized_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= max_lines:
            break

        words = line.strip().split()
        words = ["<s>"] + words + ["</s>"]

        # count unigrams
        for w in words:
            unigram_counts[w] += 1

        # count quadgrams
        for j in range(len(words) - 3):
            quadgram = (words[j], words[j+1], words[j+2], words[j+3])
            quadgram_counts[quadgram] += 1

# =========================
# Compute Probabilities
# =========================
k = [1, 10]  # Laplace and K-smoothing
V = len(unigram_counts)  # vocabulary size

quadgram_model_lap = []
quadgram_model_k = []

for (w1, w2, w3, w4), count in quadgram_counts.items():
    trigram_count = trigram_counts.get((w1, w2, w3), 0)  # denominator

    # Laplace smoothing (k=1)
    prob_lap = (count + k[0]) / (trigram_count + V * k[0])

    # General k-smoothing (k=10)
    prob_k = (count + k[1]) / (trigram_count + V * k[1])

    quadgram_model_lap.append([w1, w2, w3, w4, count, prob_lap])
    quadgram_model_k.append([w1, w2, w3, w4, count, prob_k])

# =========================
# Save Models
# =========================
quadgram_df_lap = pd.DataFrame(
    quadgram_model_lap,
    columns=["word1", "word2", "word3", "word4", "count", "prob"]
)
quadgram_df_k = pd.DataFrame(
    quadgram_model_k,
    columns=["word1", "word2", "word3", "word4", "count", "prob"]
)

quadgram_df_lap.to_csv(output_laplace, index=False, encoding="utf-8")
quadgram_df_k.to_csv(output_k, index=False, encoding="utf-8")

print("✅ Quadgram models saved (first 100,000 lines only).")
