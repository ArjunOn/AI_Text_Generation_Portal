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
# Project Workshops — AI Text Generation Portal

This document outlines an 8-session workshop series to build an AI Text Generation Portal. Each session includes a brief explanation, suggested tools, and requirements.

1. Introductions, overview of the project and set up

	 - Goal: Introduce participants, outline the workshop goals, timeline, deliverables, and verify development environments.
	 - Topics: Project goals, repo layout, roles, milestones, code of conduct, and setup steps.
	 - Requirements & Tools:
		 - Git & GitHub account
		 - Python 3.10+ installed
		 - VS Code (or preferred IDE)
		 - Node.js (optional, for web UI development)
		 - Access to AWS account (for later sessions)
	 - Pointers:
		 - Walk through the repository structure and run the sample scraper to ensure environment works.
		 - Create GitHub forks or branches per participant if necessary.

2. Web Scrapping and Data collection

	 - Goal: Collect real data to train and test models.
	 - Topics: HTTP requests, parsing HTML, rate limiting, polite scraping, and saving data.
	 - Requirements & Tools:
		 - Python libraries: requests, beautifulsoup4, pandas
		 - Optional: Selenium for dynamic pages
	 - Pointers:
		 - Show example scrapers (like `WebScraping/scraper.py`).
		 - Discuss robots.txt, rate limits, and respectful scraping practices.

3. NLP techniques, processing and understanding the data

	 - Goal: Clean and preprocess collected text data and extract useful features.
	 - Topics: Tokenization, normalization, stopword removal, stemming/lemmatization, embeddings, and exploratory data analysis.
	 - Requirements & Tools:
		 - Python libraries: nltk, spaCy, scikit-learn, pandas
		 - Jupyter or VS Code notebooks for experiments
	 - Pointers:
		 - Demonstrate EDA: word frequency, n-grams, and basic visualizations.
		 - Show how to create embeddings with spaCy or transformer models.

4. Introduction to LLMs and GPTs (creating your first model)

	 - Goal: Understand large language models and run a simple model for generation.
	 - Topics: Transformer basics, pre-trained models, fine-tuning vs prompt engineering, model inference.
	 - Requirements & Tools:
		 - Hugging Face Transformers, PyTorch or TensorFlow
		 - Access to pre-trained models via Hugging Face Hub
	 - Pointers:
		 - Start with small, local models for experiments (e.g., distilGPT-type models).
		 - Demonstrate prompt crafting and evaluate outputs.

5. Improving your model

	 - Goal: Improve output quality via data augmentation, fine-tuning, evaluation, and metrics.
	 - Topics: Fine-tuning strategies, validation/holdout sets, BLEU/ROUGE (where applicable), human evaluation.
	 - Requirements & Tools:
		 - Hugging Face Trainer or LoRA fine-tuning tools
		 - Access to GPU (local or cloud) for faster training
	 - Pointers:
		 - Show small-scale fine-tuning and measure improvements.
		 - Discuss trade-offs: compute costs vs. quality.

6. Integrating the model with a functional user interface

	 - Goal: Build a minimal web UI to interact with the model.
	 - Topics: API design, backend for inference, frontend basics (React/Flask/FastAPI), security and rate-limiting.
	 - Requirements & Tools:
		 - FastAPI or Flask for backend
		 - React or simple HTML/JS for frontend
		 - Docker (optional)
	 - Pointers:
		 - Build a small endpoint that accepts prompts and returns model outputs.
		 - Add input validation and simple usage logging.

7. AWS Deployment

	 - Goal: Deploy the model and UI to AWS for public testing.
	 - Topics: EC2, ECS/Fargate, Lambda, API Gateway, S3 for storage, IAM roles, and cost management.
	 - Requirements & Tools:
		 - AWS account and basic IAM setup
		 - AWS CLI and AWS console access
		 - Terraform or CloudFormation (optional)
	 - Pointers:
		 - Start with a small deployment (single EC2 or simple container) and iterate to more robust infra.
		 - Show how to monitor logs and set up basic alerts.

8. Final presentation and reflections

	 - Goal: Present project results, what was learned, and next steps.
	 - Topics: Demos, lessons learned, potential improvements, and future work.
	 - Requirements & Tools:
		 - Slides or demo site
		 - Recorded demo or live demo setup
	 - Pointers:
		 - Encourage participants to prepare a short demo and 3-5 key takeaways.
		 - Discuss ethical considerations and responsible AI practices.

---

## Additional resources and templates
- Example scraper: `WebScraping/scraper.py`
- Example data processing notebooks: create `notebooks/` for experiments
- Suggested reading: Hugging Face docs, spaCy tutorials, AWS deployment guides


---

If you'd like, I will commit this `readme.md` to the repo and push the changes. Should I proceed? (I will commit & push automatically if you say yes.)