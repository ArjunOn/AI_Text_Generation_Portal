# myNanoGPT — Movies dataset workspace

This folder contains the dataset, preprocessing, model scripts and checkpoints for the Movies fine-tune.

Goal
----
Keep a compact, predictable layout so you (or any collaborator) can reproduce preprocessing, training and sampling with minimal setup.

Recommended structure (the repository already follows this layout):

self_nanoGPT/ (this folder is typically named `myNanoGPT` in the repo)
- __pycache__/
- data/
  - movies/
    - input.txt             # working input (overwritten by cleaner)
    - input_clean.txt       # canonical cleaned dataset (keep this)
    - input_raw.txt         # raw backup (optional)
    - prepare.py            # creates train.bin and val.bin
    - train.bin, val.bin    # optional binaries (regenerable)
    - readme.md             # dataset notes
- out-movies/               # older checkpoint (optional)
  - ckpt.pt
- out_movies_long_ft/       # long-run checkpoint used by the UI
  - ckpt.pt                 # REQUIRED for sampling via the UI
- sample.py                 # sampling script invoked by the Flask UI
- train.py                  # training script (not required for inference)
- model.py                  # model class used by sample/train
- configurator.py           # CLI/config overrides
- logs/                     # runtime logs for training & UI (created automatically)

Logs
----
All runtime logs (training, sampling, and flask) are stored under `myNanoGPT/logs/` to keep the workspace tidy. These files are ignored by Git by default.

Notes
-----
- `train.bin` and `val.bin` are regenerable from `input_clean.txt` by running `prepare.py`, so you can archive or delete them to save space.
- Keep at least one checkpoint (e.g. `out_movies_long_ft/ckpt.pt`) if you want to serve the model with the UI.
- The Flask UI expects the checkpoint directory to contain `ckpt.pt`.

