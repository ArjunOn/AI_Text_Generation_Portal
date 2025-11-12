#!/usr/bin/env python3
"""Simple cleaning for the movies input corpus.

This script:
- backs up `data/movies/input.txt` -> `data/movies/input_raw.txt`
- strips HTML tags, unescapes HTML entities
- removes non-printable/control characters and excessive punctuation
- collapses multiple whitespace to single spaces and preserves newlines
- writes cleaned output back to `data/movies/input.txt` and also to
  `data/movies/input_clean.txt` for safety.

Run from the `myNanoGPT` folder with the environment python.
"""
import re
import html
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / 'data' / 'movies'
IN_FILE = DATA_DIR / 'input.txt'
RAW_BACKUP = DATA_DIR / 'input_raw.txt'
CLEAN_OUT = DATA_DIR / 'input_clean.txt'


def clean_text(text: str) -> str:
    # Unescape HTML entities first
    text = html.unescape(text)
    # Remove common HTML tags (naive but effective for this corpus)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Replace sequences of punctuation that look like corrupted tags
    text = re.sub(r'[\[\]{}<>/\\=*_~]+', ' ', text)
    # Remove non-printable/control characters
    text = ''.join(ch if (31 < ord(ch) < 127 or ch == '\n' or ch == '\t') else ' ' for ch in text)
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text)
    # Restore reasonable sentence breaks: ensure newlines between paragraphs
    text = re.sub(r'\s*\n\s*', '\n', text)
    # Trim
    text = text.strip()
    return text


def main():
    if not IN_FILE.exists():
        print(f'Input file not found: {IN_FILE}')
        return
    # Backup raw
    if not RAW_BACKUP.exists():
        print(f'Backing up raw input to {RAW_BACKUP}')
        IN_FILE.replace(RAW_BACKUP)
        # put RAW_BACKUP back to IN_FILE for cleaning step
        raw = RAW_BACKUP.read_text(encoding='utf-8')
    else:
        raw = IN_FILE.read_text(encoding='utf-8')

    print('Cleaning text...')
    cleaned = clean_text(raw)

    # write clean outputs
    CLEAN_OUT.write_text(cleaned, encoding='utf-8')
    # overwrite the original input.txt so prepare.py picks it up
    IN_FILE.write_text(cleaned, encoding='utf-8')
    print(f'Wrote cleaned input to {IN_FILE} and {CLEAN_OUT}')
    print(f'Original length: {len(raw):,} chars, cleaned length: {len(cleaned):,} chars')


if __name__ == '__main__':
    main()
