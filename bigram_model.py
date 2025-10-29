import pandas as pd
from collections import defaultdict

file_path = "LAB_1/tokenized_hindi.txt"

unigram_counts = defaultdict(int)
bigram_counts = defaultdict(int)

# Limit lines to first 10,000
max_lines = 100000

with open(file_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= max_lines:
            break
        words = line.strip().split()
        
        # Add start and end tokens
        words = ["<s>"] + words + ["</s>"]
        
        # Count unigrams
        for w in words:
            unigram_counts[w] += 1
        
        # Count bigrams
        for j in range(len(words) - 1):
            bigram = (words[j], words[j+1])
            bigram_counts[bigram] += 1

# Prepare models
bigram_model = []
bigram_k_model = []
k = [1, 10]
v = len(unigram_counts)

for (w1, w2), count in bigram_counts.items():
    prob_lap = (count + k[0]) / (unigram_counts[w1] + v * k[0])
    prob_k_smooth = (count + k[1]) / (unigram_counts[w1] + v * k[1])
    
    bigram_model.append([w1, w2, count, prob_lap])
    bigram_k_model.append([w1, w2, count, prob_k_smooth])

# Convert to DataFrame
bigram_df = pd.DataFrame(bigram_model, columns=["word1", "word2", "count", "prob"])
bigram_k_df = pd.DataFrame(bigram_k_model, columns=["word1", "word2", "count", "prob"])

# Save to CSV
bigram_df.to_csv("LAB_4/Bigram_Model/bigram_model_laplace_smoothing.csv", index=False, encoding="utf-8")
bigram_k_df.to_csv("LAB_4/Bigram_Model/bigram_model_k_smoothing.csv", index=False, encoding="utf-8")

print("Bigram models saved successfully.")
