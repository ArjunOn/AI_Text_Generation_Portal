# nanoGPT Flask Web Application

A web-based text generation application using nanoGPT models trained on multiple datasets (Movies and Twitter).

## 🎯 Project Overview

This project provides an intuitive web interface for generating text using trained nanoGPT language models. Users can select different datasets and generate creative text with a single click.

## 📁 Project Structure
```
nanoGPT-flask-app/
├── .venv/                    # (Keep but don't push to GitHub)
├── data/
│   ├── movies/
│   │   ├── input.txt
│   │   ├── train.bin
│   │   └── val.bin
│   └── twitter/
│       ├── input.txt
│       ├── train.bin
│       └── val.bin
├── out-movies/
│   └── ckpt.pt
├── out-twitter/
│   └── ckpt.pt
├── app.py
├── config.py
├── configurator.py
├── index.html
├── model.py
├── prepare.py
├── sample.py
└── train.py
```

## Quick start (how I run the UI)

I keep the UI intentionally small and local — a single-file Flask backend (`app.py`) tying the frontend (`index.html`) to the sampling script inside `myNanoGPT/`.

What I do locally to run it:

1) Activate your Python environment (the project uses the virtualenv under `Modelling/nanoGPT/.venv` in my setup).

2) Start the app from the repo root (so paths resolve):

```powershell
cd A:\Projects\AI_Text_Generation_Portal\nanoGPT-flask-app
# use the venv python you installed dependencies into
A:\Projects\AI_Text_Generation_Portal\Modelling\nanoGPT\.venv\Scripts\python.exe app.py
```

3) Open http://127.0.0.1:5000 in your browser. The UI will fetch available checkpoint folders from `myNanoGPT/` and auto-select the latest checkpoint.

Where logs go
---------------
To keep the folders tidy, runtime logs are written into `myNanoGPT/logs/` (the Flask app creates this folder automatically). The repo's `.gitignore` excludes these logs so the repo doesn't bloat with training artifacts.

Checkpoints
-----------
The UI looks for `ckpt.pt` inside the checkpoint folders (names matching `out_*`). Keep at least one checkpoint (for example `out_movies_long_ft/ckpt.pt`) if you want to generate text.

Notes
-----
- The UI now supports selecting an explicit checkpoint (not just dataset), and the backend uses a fresh random seed for each generation so repeated clicks produce varied outputs.
