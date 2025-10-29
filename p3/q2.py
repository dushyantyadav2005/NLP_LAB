import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import json
from pathlib import Path

# ==== CONFIG ====
DATA_PATH = Path(r"C:\Users\adity\Desktop\Sem 5\NLP\Assignment_01\hindi_tokenized_words.csv")
CHUNKSIZE = 100000   # number of rows per chunk (tune if memory allows)
OUTPUT_DIR = DATA_PATH.parent / "assignment3_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Reading file in chunks from:", DATA_PATH)

# ==== Step 1: Count frequencies efficiently ====
freq_counter = Counter()
total_tokens = 0

for chunk in pd.read_csv(DATA_PATH, chunksize=CHUNKSIZE):
    # Assuming each row has a column 'word' containing the token
    # If your file has a different column name, replace 'word' below
    colname = chunk.columns[0]   # take first column if unsure
    tokens = chunk[colname].astype(str).str.strip().tolist()
    freq_counter.update(tokens)
    total_tokens += len(tokens)

print(f"Total tokens processed: {total_tokens:,}")
print(f"Unique tokens: {len(freq_counter):,}")

# ==== Step 2: Save frequency distribution ====
freq_list = sorted(freq_counter.items(), key=lambda x: x[1], reverse=True)
top_100 = freq_list[:100]

freq_csv = OUTPUT_DIR / "q2_freq_distribution.csv"
pd.DataFrame(freq_list, columns=["token","count"]).to_csv(freq_csv, index=False, encoding="utf-8")
print("Full frequency distribution saved to:", freq_csv)

# ==== Step 3: Plot top-100 tokens ====
plt.figure(figsize=(12,6))
tokens_plot = [t for t,c in top_100]
counts_plot = [c for t,c in top_100]
plt.bar(range(len(tokens_plot)), counts_plot)
plt.xticks(range(len(tokens_plot)), tokens_plot, rotation=90)
plt.title("Top 100 tokens by frequency (Assignment-3 Q2)")
plt.tight_layout()
plot_top100 = OUTPUT_DIR / "q2_top100.png"
plt.savefig(plot_top100)
plt.close()
print("Top-100 plot saved to:", plot_top100)

# ==== Step 4: Stopword removal using thresholds ====
max_freq = freq_list[0][1]
thresholds = [
    int(max_freq * 0.05),  # 5% of max frequency
    int(max_freq * 0.02),  # 2% of max frequency
    int(max_freq * 0.01)   # 1% of max frequency
]

removed_stats = []

for th in thresholds:
    filtered = [(t,c) for t,c in freq_list if c <= th]
    top100_filtered = filtered[:100]

    # Save plot
    plt.figure(figsize=(12,6))
    toks = [t for t,c in top100_filtered]
    cnts = [c for t,c in top100_filtered]
    plt.bar(range(len(toks)), cnts)
    plt.xticks(range(len(toks)), toks, rotation=90)
    plt.title(f"Top tokens after removing stopwords with freq > {th}")
    plt.tight_layout()
    ppath = OUTPUT_DIR / f"q2_top_after_th_{th}.png"
    plt.savefig(ppath)
    plt.close()

    # Record stats
    removed = sum(c for t,c in freq_list if c > th)
    removed_stats.append({
        "threshold": th,
        "removed_tokens_count": removed,
        "remaining_unique": len(filtered)
    })

    print(f"Stopword removal threshold {th}: removed {removed:,} tokens, remaining unique={len(filtered):,}")
    print("Plot saved to:", ppath)

# ==== Step 5: Save summary JSON ====
summary_json = OUTPUT_DIR / "q2_summary.json"
with open(summary_json, "w", encoding="utf-8") as f:
    json.dump({
        "total_tokens": total_tokens,
        "unique_tokens": len(freq_counter),
        "top_100": top_100,
        "thresholds": thresholds,
        "removed_stats": removed_stats
    }, f, ensure_ascii=False, indent=2)

print("Summary JSON saved to:", summary_json)
print("=== DONE ===")
