import re


def sentence_tokenizer(paragraph):
  pattern='[\u0964!?.][^0-9.0-9]'
  sentences=re.split(pattern,paragraph)
  ends=re.findall(pattern,paragraph)
  res=[]
  for sentence in sentences:
    if ends==[]:
      break
    end=ends.pop(0)
    res.append(sentence.strip() + end)
  return res


def word_tokenizer(sentence):
    url_pattern = r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(?:\+?[0-9\u0966-\u096F]{1,3}[\s-]?)?[0-9\u0966-\u096F]{10}'
    time_pattern = r'[0-9\u0966-\u096F]{1,2}:[0-9\u0966-\u096F]{2}'
    latin_number = r'[0-9]+(?:\.[0-9]+)?'
    devnag_number = r'[\u0966-\u096F]+(?:\.[\u0966-\u096F]+)?'
    punctuation = r'[!?\.\u0964\,"\'\+-]'
    hindi_word = fr'[\u0900-\u0963\u0965-\u096F]+[^!?\.\u0964\,"\'\+-]'
    english_word = r'[a-zA-Z]+'
    emoji_pattern = r'[\U0001F300-\U0001FAFF\U00002700-\U000027BF]'
    pattern = fr'{email_pattern}|{url_pattern}|{phone_pattern}|{time_pattern}|{latin_number}|{devnag_number}|{punctuation}|{hindi_word}|{emoji_pattern}|{english_word}'

    return re.findall(pattern, sentence)
from datasets import load_dataset
from tqdm import tqdm

dataset = load_dataset("ai4bharat/IndicCorpV2", "indiccorp_v2", split="hin_Deva", streaming=True)


output_file = "tokenized_hindi.txt"
max_lines = 10_000  # Limit to 10,000 lines
line_count = 0

with open(output_file, "w", encoding="utf-8") as fout:
    for row in tqdm(dataset, desc="Tokenizing dataset"):
        if line_count >= max_lines:
            break

        text = row['text']
        sentences = sentence_tokenizer(text)
        for sent in sentences:
            tokens = word_tokenizer(sent)
            fout.write(" ".join(tokens) + "\n")
            line_count += 1

            if line_count >= max_lines:
                break
