#!/usr/bin/env python3
"""Aggressive cleaner for the movies corpus.

Creates `input_clean.txt` from `input_raw.txt` (or `input.txt` if raw missing).
This cleaner:
- fully unescapes HTML entities
- removes HTML tags using regex
- removes sequences of angle-bracket-like tokens and xml/html entities
- strips leftover markup tokens like <b>, </span>, &nbsp;, etc.
- removes isolated symbols (@, $, ^, %), excessive repeated punctuation, and control chars
- preserves sentence punctuation (.,!?;:) and newlines, collapses repeated spaces

Also prints small before/after snippets for quick inspection.
"""
import re
import html
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / 'data' / 'movies'
RAW = DATA_DIR / 'input_raw.txt'
IN = DATA_DIR / 'input.txt'
OUT = DATA_DIR / 'input_clean.txt'


def aggressive_clean(text: str) -> str:
    # unescape HTML entities
    text = html.unescape(text)
    # remove common HTML tags and attributes
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.S|re.I)
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.S|re.I)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.S)
    # remove all tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # remove bracketed annotations like [applause], (laughs)
    text = re.sub(r'\[[^\]]+\]', ' ', text)
    text = re.sub(r'\([^\)]+\)', ' ', text)
    # remove leftover tokens with lots of punctuation or weird chars
    text = re.sub(r'[\[\]{}|\\/=_*~]+', ' ', text)
    # remove sequences of @ $ % ^ & * ~ that appear noisy
    text = re.sub(r'[@$%^&+=*~]+', ' ', text)
    # remove HTML entities leftover like &nbsp;
    text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)
    # remove non-printable/control characters except newline and tab
    text = ''.join(ch if (31 < ord(ch) < 127 or ch in '\n\t') else ' ' for ch in text)
    # collapse multiple punctuation to single (except keep sentence enders)
    text = re.sub(r'([!?.]){2,}', r'\1', text)
    # remove runs of non-word punctuation (e.g. '^^^', '***', '%%%')
    text = re.sub(r'[^\w\s]{2,}', ' ', text)
    # remove isolated single punctuation tokens that appear between spaces (e.g. ' @ ', ' $ ')
    text = re.sub(r'(?<=\s)[^\w\s](?=\s)', ' ', text)
    # normalize smart quotes and similar characters to ascii equivalents
    text = text.replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    # keep only basic punctuation and alphanumerics, preserving sentence punctuation and newlines
    text = re.sub(r'[^\w\s\.,!\?;:\'"\-\(\)]', ' ', text)
    # remove isolated single-letter tokens except the valid words 'a' and 'I'
    text = re.sub(r'(?<=\s)(?!(?:a|I)\b)[A-Za-z](?=\s)', ' ', text)
    # collapse whitespace
    text = re.sub(r'[ \t\f\v]+', ' ', text)
    text = re.sub(r'\s*\n\s*', '\n', text)
    # strip leading/trailing
    return text.strip()


def main():
    if RAW.exists():
        src = RAW.read_text(encoding='utf-8')
        print(f'Using backup raw: {RAW}')
    elif IN.exists():
        src = IN.read_text(encoding='utf-8')
        print(f'Raw backup not found, using current input: {IN}')
    else:
        print('No input file found.')
        return

    print('Original sample (first 400 chars):')
    print(src[:400].replace('\n','\\n'))

    cleaned = aggressive_clean(src)

    print('\nCleaned sample (first 400 chars):')
    print(cleaned[:400].replace('\n','\\n'))

    OUT.write_text(cleaned, encoding='utf-8')
    # overwrite working input.txt so prepare.py picks it up
    IN.write_text(cleaned, encoding='utf-8')
    print(f'Wrote cleaned input to {OUT} and replaced {IN}')
    print(f'Original length: {len(src):,}, cleaned length: {len(cleaned):,}')


if __name__ == '__main__':
    main()
