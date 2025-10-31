# Modelling — nanoGPT assignment

This folder collects the files, data, experiments and results for the nanoGPT assignment performed inside this project. It documents how the data was prepared, how the models were trained and where to find the outputs and logs.

## Summary
- Source project: a fork/clone of nanoGPT (kept as a submodule at `Modelling/nanoGPT_project`).
- Goal: prepare a cleaned Twitter corpus, tokenize it, run short sanity and longer training experiments on CPU, generate example samples, and collect logs and artifacts under this repository.

## What I prepared and where
- Copied assignment assets (so they are tracked by the main repo) into:
  - `Modelling/nanoGPT_assignment/`
    - `data/custom_corpus/cleaned_twitter_corpus.txt` — cleaned text corpus used for training
    - `data/custom_corpus/prepare.py` — tokenizer/prepare script (uses tiktoken/gpt2)
    - `data/custom_corpus/train.bin`, `val.bin` — tokenized dataset (uint16 arrays)
    - `data/custom_corpus/meta.pkl` — token metadata (stoi/itos/vocab_size)
    - `config/train_custom.py` — training config for this dataset
    - `sample.py` and `sample_safe.py` — sampling scripts (safe decoder helper included)

- The original nanoGPT clone remains as a submodule at `Modelling/nanoGPT_project/` and contains full project files, `.venv`, and the produced checkpoints.

## Experiments and logs
- Experiments and generated samples are stored in:
  - `Modelling/experiments/experiments/training_runs/` — training logs and sampling outputs
  - `Modelling/experiments/experiments/samples/generated_examples.txt` — initial generated examples

- A long CPU training run was executed and its log (2000 iters) is here:
  - `Modelling/experiments/experiments/training_runs/long_run.log`

The exact checkpoint files produced by the nanoGPT training runs live inside the submodule directories (not copied into the main repo):
- `Modelling/nanoGPT_project/out-custom* / out-custom-long/ckpt.pt`

Note: checkpoints were left inside the nanoGPT submodule to avoid bloating the main repository with large binaries. If you want a checkpoint copied into `Modelling/experiments/` or uploaded somewhere, tell me and I will do it.

## Environment
- Python: the nanoGPT project used a virtual environment at `Modelling/nanoGPT_project/.venv` (Python 3.12.x in this session).
- Key packages (installed into the project venv): torch, numpy, tiktoken, transformers, datasets, wandb, tqdm.
- To use the venv Python on Windows (PowerShell):
  - `& .\Modelling\nanoGPT_project\.venv\Scripts\python.exe <script>`

## Reproduce locally (quick guide)

1) Prepare dataset (inside the assignment folder or the nanoGPT project):

```powershell
Set-Location .\Modelling\nanoGPT_assignment
& ..\nanoGPT_project\.venv\Scripts\python.exe .\data\custom_corpus\prepare.py
```

This writes `train.bin`, `val.bin` and `meta.pkl` into `data/custom_corpus` (already present in the repo copy).

2) Run training (example short sanity run)

```powershell
Set-Location .\Modelling\nanoGPT_project
& .\.venv\Scripts\python.exe train.py config\train_custom.py --device=cpu --compile=False --eval_iters=10 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=2 --n_head=2 --n_embd=64 --max_iters=200 --lr_decay_iters=200 --dropout=0.0
```

3) Run a longer CPU run (what we executed):

```powershell
Set-Location .\Modelling\nanoGPT_project
& .\.venv\Scripts\python.exe train.py config\train_custom.py --device=cpu --compile=False --eval_interval=200 --eval_iters=20 --log_interval=10 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0 --out_dir=out-custom-long --always_save_checkpoint=True
```

4) Sample from a checkpoint (using `sample.py`, which will use `meta.pkl` if present):

```powershell
Set-Location .\Modelling\nanoGPT_project
& .\.venv\Scripts\python.exe sample.py --out_dir=out-custom-long --device=cpu --num_samples=3 --max_new_tokens=120
```

If `sample.py` fails to decode some tokens (token id mismatch), use `sample_safe.py` which substitutes unknown token ids with `<|UNK|>` and writes examples to `out_dir/samples/generated_examples.txt`.

## Results (high level)
- Short sanity run (200 iters): train loss dropped from ~10.8 → ~6.9.
- Longer runs (200 iterations, several variants) showed further loss reduction.
- Long CPU run (2000 iters, config above) final reported training loss (approx): ~3.6 (see `long_run.log`). Validation loss remained higher / noisier in our small experiments — check the logs for detailed numeric traces and per-eval checkpoints.

## Notes and recommendations
- CPU runs are useful for quick experiments, but are slow for larger models. For meaningful scale-up (larger n_layer/n_embd and higher iterations) use a GPU.
- Checkpoints are large — we left them in the submodule (`Modelling/nanoGPT_project/out-*`). If you want them archived in the main repo or uploaded to a release or cloud storage, I can help with that.
- If you plan to reproduce or extend the work, consider:
  - Creating a small script under `Modelling/nanoGPT_assignment/` that automates venv activation, prepare, train and sample steps.
  - Adding a `requirements.txt` that matches the `.venv` used for experiments if you want reproducible installs outside the `uv` workflow.

## Files and locations (quick index)
- Main assignment tracked in repo: `Modelling/nanoGPT_assignment/`
- Full nanoGPT clone (submodule): `Modelling/nanoGPT_project/`
- Experiments and logs: `Modelling/experiments/experiments/training_runs/` and `Modelling/experiments/experiments/samples/`
- Analysis notes: `Modelling/analysis_notes.txt`

---

Reproducibility helpers (added)

I added a few small helper files to make reproducing the prepare → train → sample workflow easier from the main repo:

- `Modelling/init_submodule.ps1` — Initializes and updates the `Modelling/nanoGPT_project` submodule and lists available `out-*` directories (where checkpoints live).
- `Modelling/nanoGPT_assignment/run_all.ps1` — A convenience PowerShell script that:
  - runs the `prepare.py` tokenizer to (re)create `train.bin`, `val.bin`, `meta.pkl` inside the assignment copy;
  - runs a short sanity training session (small model / few iterations) from the nanoGPT project venv to validate end-to-end; and
  - runs `sample_safe.py` to produce a few generated examples into the selected `out_dir`.
- `Modelling/nanoGPT_assignment/requirements.txt` — list of core packages used by the experiments (useful if you want to recreate a venv outside the project `.venv`).

Checkpoint policy

Checkpoints produced by training are intentionally left in the nanoGPT submodule under `Modelling/nanoGPT_project/out-*` to avoid adding large binaries to the main repository. This keeps the main repo lightweight and reproducible. If you'd like me to copy a specific checkpoint into `Modelling/experiments/` (or upload it to a release or cloud storage), tell me which one and I'll do that.

How to use the helpers

1) Initialize the submodule (runs `git submodule update --init --recursive`):

```powershell
Set-Location A:\Projects\AI_Text_Generation_Portal
& .\Modelling\init_submodule.ps1
```

2) Run the end-to-end reproducibility script (will call the project venv Python if available):

```powershell
Set-Location A:\Projects\AI_Text_Generation_Portal
& .\Modelling\nanoGPT_assignment\run_all.ps1
```

The `run_all.ps1` script uses the nanoGPT project's venv at `Modelling/nanoGPT_project/.venv\Scripts\python.exe` if present; otherwise it falls back to `python` on PATH. It runs a short sanity training (fast) by default so you can validate the full flow quickly. Modify the script to change hyperparameters or `max_iters` if you want a longer run.

Flattening the experiments folder

I will now flatten the nested `Modelling/experiments/experiments/` into `Modelling/experiments/` so the logs and samples are at a single predictable path. The original nested folder will be removed after the move. If you prefer I preserve the nested structure or instead archive the current structure, tell me and I will revert.

Generated on: 2025-10-30
