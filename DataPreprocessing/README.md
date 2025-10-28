# Data Preprocessing

This folder contains starter tools for preprocessing scraped data before feeding it to NLP models.

Files
- `preprocess.py` - small script to normalize text and numeric fields from the scraped CSV.
- `processed_country_data.csv` - output produced after running the script (not committed by default; only here if produced locally).

How to run

From the repository root (PowerShell):

```powershell
cd A:\Projects\AI_Text_Generation_Portal\datapreprocessing
# uses the CSV produced by WebScraping/scraper.py
python preprocess.py --input ..\WebScraping\country_data.csv --output processed_country_data.csv
```

What it does
- Lowercases and trims textual fields (Name, Capital).
- Attempts to parse Population and Area into integers and adds `Population_clean` and `Area_clean` columns.

Dependencies
- pandas (already used elsewhere in the project)

Notes
- This is intentionally small and dependency-light. For production/complex preprocessing, expand with `nltk`/`spaCy` pipelines, tokenization, and more robust numeric parsing.
