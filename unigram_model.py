import pandas as pd

# ================================
# Load word frequencies
# ================================
df = pd.read_csv("LAB_3/word_freq.csv")
stats = pd.read_csv("hindi_text_statistics.csv")

total_tokens = df["freq"].sum()
V = len(df)
num_sentences = int(stats.loc[0, "Total Sentences"])

# ================================
# Function to build unigram model
# ================================
def build_unigram_model(k, out_file):
    print(f"Processing Unigram Model with k={k}...")

    unigram_data = []
    for _, row in df.iterrows():
        word = row["word"]
        count = row["freq"]
        prob = (count + k) / (total_tokens + k * (V + 2))  # +2 for <s>, </s>
        unigram_data.append([word, count, prob])

    # Add <s>
    prob_s = (num_sentences + k) / (total_tokens + k * (V + 2))
    unigram_data.append(["<s>", num_sentences, prob_s])

    # Add </s>
    prob_es = (num_sentences + k) / (total_tokens + k * (V + 2))
    unigram_data.append(["</s>", num_sentences, prob_es])

    # Save file
    uni_df = pd.DataFrame(unigram_data, columns=["word", "count", "prob"])
    uni_df.to_csv(out_file, index=False, encoding="utf-8")
    print(f"Saved {out_file}")


# ================================
# Build models for k=0,1,10
# ================================
build_unigram_model(0, "LAB_4/Unigram_Model/unigram_model.csv")
build_unigram_model(1, "LAB_4/Unigram_Model/unigram_model_laplace_smoothing.csv")
build_unigram_model(10, "LAB_4/Unigram_Model/unigram_model_k_smoothing.csv")
