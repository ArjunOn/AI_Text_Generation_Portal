import re
import argparse
from typing import List

# NLTK imports are inside functions to allow graceful fallback if not installed

def read_lines(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return [line.rstrip('\n') for line in f]


def clean_text(text: str) -> str:
    """Apply regex-based cleaning to a tweet string."""
    if not text:
        return ""
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    # Remove HTML tags / entities (basic)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace('&amp;', 'and')
    # Remove Twitter handles
    text = re.sub(r"@\w+", "", text)
    # Remove RT marker (at start or standalone)
    text = re.sub(r"\brt\b", "", text)
    # Remove non-letter characters (keep spaces)
    text = re.sub(r"[^a-z\s]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def process_tokens(text: str) -> List[str]:
    """Tokenize, remove stopwords, and lemmatize using NLTK.

    Falls back to a simple split if NLTK isn't available.
    """
    try:
        import nltk
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        from nltk.tokenize import word_tokenize
    except Exception:
        # fallback tokenizer
        tokens = text.split()
        return tokens

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # tokenize
    tokens = word_tokenize(text)

    processed = []
    for t in tokens:
        t = t.lower().strip()
        if not t or t in stop_words:
            continue
        # lemmatize
        lemma = lemmatizer.lemmatize(t)
        if lemma and lemma not in stop_words:
            processed.append(lemma)
    return processed


def main(input_path: str, output_path: str):
    lines = read_lines(input_path)
    cleaned_lines = []

    for line in lines:
        c = clean_text(line)
        tokens = process_tokens(c)
        cleaned = " ".join(tokens)
        cleaned_lines.append(cleaned)

    # Print comparison for first 5
    n_preview = min(5, len(lines))
    print("\nFirst 5 raw -> processed samples:\n")
    for i in range(n_preview):
        print(f"RAW {i+1}: {lines[i]}")
        print(f"PROC {i+1}: {cleaned_lines[i]}\n")

    # Write output
    with open(output_path, 'w', encoding='utf-8') as outf:
        for l in cleaned_lines:
            outf.write(l + '\n')

    print(f"Wrote {len(cleaned_lines)} cleaned lines to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', default='DataPreprocessing/corrupt_twitter_corpus.txt')
    parser.add_argument('--output', '-o', default='DataPreprocessing/cleaned_twitter_corpus.txt')
    args = parser.parse_args()
    main(args.input, args.output)
