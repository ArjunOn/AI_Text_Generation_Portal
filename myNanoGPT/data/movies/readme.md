
# Movies dataset

This folder contains the raw and cleaned movie dialogue/text used to fine-tune a small nanoGPT model.

Files of interest:
- `input_raw.txt` — original raw text backup (kept for reference)
- `input_clean.txt` — the cleaned, canonical dataset (this is what `prepare.py` uses)
- `input.txt` — a working copy that `prepare.py` will read; the cleaner script can overwrite this
- `prepare.py` — converts `input_clean.txt` into `train.bin` and `val.bin` (tokenized binaries)
- `train.bin` / `val.bin` — tokenized binary files used for training; these are regenerable from `input_clean.txt` if you need to save space

Quick notes
- Keep `input_clean.txt` as the canonical source of truth for preprocessing. If you need to re-run tokenization, run `python prepare.py` from this folder.
- The README here is intentionally short — the main `myNanoGPT/README.md` describes where logs and checkpoints land and how the Flask UI connects to the latest checkpoint.
