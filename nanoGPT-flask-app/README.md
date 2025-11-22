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

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- UV package manager (or pip)
- 8GB+ RAM recommended
- GPU optional (for faster generation)

### Installation

1. **Clone the repository**
```bash
   git clone <repo-url>
   cd nanoGPT-flask-app
```

2. **Set up virtual environment**
```bash
   # Using UV
   uv venv
   # Activate
   .venv\Scripts\activate      # On Windows
   # Install dependencies
   uv add flask
```

3. **Run the application**
```bash
python app.py
```

4. **Open in browser**
Navigate to: http://localhost:5000

## 🎮 Usage

1. **Select Dataset**: Choose between Movies or Twitter dataset from the dropdown
2. **Generate Text**: Click the "Generate Text" button
3. **View Output**: Generated text will appear in the output area
4. **Generate Again**: Click the button again to generate new text

## 🔧 Training New Models

Follow the instructions in the repo to prepare data, run `prepare.py`, and train with `train.py`.

## ⚙️ Configuration

Edit `config.py` to modify training and model hyperparameters.

## 🛠️ Troubleshooting

- If Flask not installed: `uv add flask`
- If model not found: ensure checkpoint folders exist or run training

---

