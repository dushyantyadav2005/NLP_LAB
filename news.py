import requests
import pandas as pd
from LAB_1.tokenizer import sentence_tokenizer   
from LAB_1.tokenizer import word_tokenizer
from news_utils import sentence_probability   

# ================================
# CONFIG
# ================================
API_KEY = "YOUR_NEWSAPI_KEY"  
URL = "https://newsapi.org/v2/everything"
QUERY = "भारत"   # Hindi keyword for India news
LANG = "hi"
MAX_SENTENCES = 1000

# ================================
# Fetch News from NewsAPI
# ================================
def fetch_hindi_news():
    all_sentences = []
    page = 1

    while len(all_sentences) < MAX_SENTENCES:
        params = {
            "apiKey": API_KEY,
            "q": QUERY,
            "language": LANG,
            "pageSize": 100,
            "page": page
        }
        response = requests.get(URL, params=params)
        data = response.json()

        if "articles" not in data or len(data["articles"]) == 0:
            break

        for article in data["articles"]:
            if article["content"]:
                sentences = sentence_tokenizer(article["content"])
                all_sentences.extend(sentences)

        page += 1

    return all_sentences[:MAX_SENTENCES]

# ================================
# Process sentences
# ================================
def process_sentences(sentences):
    results = []
    for sent in sentences:
        probs = {
            "unigram_prob": sentence_probability(sent, model="unigram"),
            "bigram_prob": sentence_probability(sent, model="bigram"),
            "trigram_prob": sentence_probability(sent, model="trigram"),
            "quadgram_prob": sentence_probability(sent, model="quadgram"),
        }
        results.append({
            "sentence": sent,
            **probs
        })
    return results

# ================================
# MAIN
# ================================
if __name__ == "__main__":
    print("Fetching Hindi news...")
    sentences = fetch_hindi_news()
    print(f"Collected {len(sentences)} sentences.")

    print("Calculating sentence probabilities...")
    results = process_sentences(sentences)

    df = pd.DataFrame(results)
    df.to_csv("LAB_4/news_sentence_probs.csv", index=False, encoding="utf-8-sig")

    print("Done. Saved to LAB_4/news_sentence_probs.csv")
