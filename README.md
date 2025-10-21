# AI_Text_Generation_Portal

This repository contains a small web scraper that extracts country data from a static demo site and writes it to CSV.

## What it does
- Fetches HTML from `https://www.scrapethissite.com/pages/simple/`.
- Parses country entries and extracts: Name, Capital, Population, Area.
- Writes the data to `country_data.csv` in the `WebScraping` folder.

## Files
- `WebScraping/scraper.py` - the scraping script.
- `WebScraping/country_data.csv` - output CSV produced by the script (example run).

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
python WebScraping/scraper.py
```

The script will write `country_data.csv` in the `WebScraping` folder.

## Notes
- Population and Area are left as strings as presented on the page; you may want to normalize them to numeric types.
- The script is written for educational/demo purposes and targets a static demo site.

## Pushing to GitHub
I attempted to create and push the repository automatically; if that failed, follow these steps:

1. Create a new repository on GitHub named `AI_Text_Generation_Portal`.
2. Then run:

```powershell
cd A:\Projects\AI_Text_Generation_Portal
git init
git add .
git commit -m "Initial commit: add scraper and README"
git branch -M main
git remote add origin https://github.com/<your-username>/AI_Text_Generation_Portal.git
git push -u origin main
```

Replace `<your-username>` with your GitHub username.

If you want, I can attempt to create the repo and push it from here (requires GitHub CLI or personal access token configured).