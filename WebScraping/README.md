# Webscraping

This folder contains a small web scraper that extracts country data from a static demo site and writes it to CSV.

## What it does
- Fetches HTML from `https://www.scrapethissite.com/pages/simple/`.
- Parses country entries and extracts: Name, Capital, Population, Area.
- Writes the data to `country_data.csv` in this folder.

## Files
- `scraper.py` - the scraping script.
- `country_data.csv` - output CSV produced by the script (example run).

## Python packages used
- requests
- beautifulsoup4
- pandas

Install packages (uses the system python executable):

```powershell
# install with uv if you use the uv tool, otherwise use python -m pip
uv pip install beautifulsoup4 requests pandas; if ($LASTEXITCODE -ne 0) { python -m pip install beautifulsoup4 requests pandas }
```

## Usage
Run the scraper with Python (example):

```powershell
python scraper.py
```

The script will write `country_data.csv` in this folder.

## Notes
- Population and Area are left as strings as presented on the page; you may want to normalize them to numeric types.
- The script is written for educational/demo purposes and targets a static demo site.
