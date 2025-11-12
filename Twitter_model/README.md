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
## Modelling — nanoGPT assignment (summary for the team)

This document explains, at a team level, what was done for the nanoGPT modelling assignment, what the results were, and how you can reproduce or extend the work. It's written for the project lead and fellow contributors who will run the same workflow or inspect the experiments.

### Short contract
- Inputs: cleaned Twitter corpus located under `Modelling/nanoGPT_assignment/data/custom_corpus/` (text file, tokenizer/prepare script available).
- Outputs: tokenized datasets (`train.bin`, `val.bin`, `meta.pkl`), training logs, generated samples, and checkpoints stored in the nanoGPT submodule `Modelling/nanoGPT_project/out-*`.
- Success criteria: end-to-end reproducible prepare → train → sample flow; decreased training loss in sanity and longer runs; saved logs and generated examples for review.

### What lives in this folder (quick index)
- `Modelling/nanoGPT_assignment/` — assignment files tracked in the main repo (data copy, prepare script, small helpers).
- `Modelling/nanoGPT_project/` — full nanoGPT clone kept as a submodule (contains `.venv`, training code, and large checkpoints in `out-*`).
- `Modelling/experiments/` — logs and generated samples (flattened path). See `training_runs/` and `samples/` inside.

If you're reading this to reproduce or extend experiments, the most important files are:
- `Modelling/nanoGPT_assignment/data/custom_corpus/cleaned_twitter_corpus.txt` — original cleaned text used for training.
- `Modelling/nanoGPT_assignment/data/custom_corpus/prepare.py` — tokenization and serialization to `train.bin`, `val.bin`, and `meta.pkl` (uses tiktoken/gpt2 encoding by default).
- `Modelling/nanoGPT_assignment/config/train_custom.py` — example training config used in experiments.

### High level process we followed
1. Data cleaning and normalization (result: `cleaned_twitter_corpus.txt`). Steps included removing duplicates, normalizing whitespace, replacing or removing undesirable tokens (URLs and excessive mentions), and ensuring UTF-8 cleanliness.
2. Tokenization: ran `prepare.py` which uses tiktoken (GPT-2 tokenizer) to produce `train.bin`, `val.bin` and `meta.pkl` (stoi/itos + vocab size). The provided script is configurable and will re-create the binaries when rerun.
3. Experiments: executed short sanity runs and a longer CPU training run (2000 iterations) using the nanoGPT training loop. Hyperparameters are recorded in `config/train_custom.py` or passed on the CLI for ad-hoc runs.
4. Sampling: used `sample.py` / `sample_safe.py` to generate text from checkpoints. `sample_safe.py` is more resilient to token id mismatches and writes outputs into `out_dir/samples/`.

### Key experiments and results (concise)
- Short sanity training (max_iters=200, small model): training loss dropped from ~10.8 → ~6.9. This validated the training loop and dataset.
- Longer CPU run (max_iters=2000, medium model config): reported final training loss ≈ 3.6 (see `Modelling/experiments/training_runs/long_run.log`). Validation loss was higher and noisier — our dataset and evaluation settings are small, so expect variance.

Notes on results interpretation:
- Loss numbers here are indicative; they depend heavily on sequence length, batch size, and whether we use learning-rate scheduling. Use the log files for per-iteration traces and to compare different runs.
- Generated samples are in `Modelling/experiments/samples/` — review them qualitatively for repetition, coherence, and safety.

### Environment used
- Python: the nanoGPT project used a venv in `Modelling/nanoGPT_project/.venv` (Python 3.12.x during experiments).
- Important packages: torch (CPU builds were used), numpy, tiktoken, transformers, datasets, wandb (optional), tqdm.
- On Windows PowerShell you can run the venv Python with:

    & .\Modelling\nanoGPT_project\.venv\Scripts\python.exe <script>

If you don't have the submodule `.venv`, follow the reproduce steps below to create a venv and install requirements.

### Reproduce locally (minimal steps)
Run these steps from the repo root `A:\Projects\AI_Text_Generation_Portal` using PowerShell.

1) Initialize submodule (only first time):

```powershell
Set-Location A:\Projects\AI_Text_Generation_Portal
& .\Modelling\init_submodule.ps1
```

2) Prepare the dataset (creates `train.bin`, `val.bin`, `meta.pkl`):

```powershell
Set-Location .\Modelling\nanoGPT_assignment
& ..\nanoGPT_project\.venv\Scripts\python.exe .\data\custom_corpus\prepare.py
```

3) Run a short sanity training to validate end-to-end (uses project venv):

```powershell
Set-Location .\Modelling\nanoGPT_project
& .\.venv\Scripts\python.exe train.py config\train_custom.py --device=cpu --compile=False --eval_iters=10 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=2 --n_head=2 --n_embd=64 --max_iters=200 --lr_decay_iters=200 --dropout=0.0
```

4) Run the longer CPU run we used (optional — slow on CPU):

```powershell
Set-Location .\Modelling\nanoGPT_project
& .\.venv\Scripts\python.exe train.py config\train_custom.py --device=cpu --compile=False --eval_interval=200 --eval_iters=20 --log_interval=10 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0 --out_dir=out-custom-long --always_save_checkpoint=True
```

5) Sample from a checkpoint:

```powershell
Set-Location .\Modelling\nanoGPT_project
& .\.venv\Scripts\python.exe sample.py --out_dir=out-custom-long --device=cpu --num_samples=3 --max_new_tokens=120
```

Use `sample_safe.py` if you encounter token id mismatches.

### Short troubleshooting / gotchas
- Tokenizer/version mismatches: if you see unknown token ids during sampling, use `sample_safe.py` or re-run `prepare.py` with the same tokenizer version used for training.
- Checkpoint size: checkpoints can be large; they currently remain in the submodule to keep the main repo lightweight.
- CPU training is slow; for more than toy experiments use a GPU.

### Quick checklist for someone reproducing this work
- [ ] Initialize submodule and venv
- [ ] Run `prepare.py` to produce tokenized binaries
- [ ] Run short sanity training (small model, few iterations)
- [ ] Run sampling and inspect generated examples
- [ ] If desired, run longer training with adjusted hyperparameters on a GPU

### Recommended next steps (technical and project)
1. Add a small orchestration script in `Modelling/nanoGPT_assignment/` that wraps submodule init, venv creation, prepare, train (sanity), and sample — this reduces manual steps for reviewers.
2. Add a pinned `requirements.txt` that matches the venv used for experiments to improve reproducibility outside the submodule venv.
3. If checkpoints should be shared with the team, either copy selected checkpoint files into `Modelling/experiments/` or upload to cloud storage and add links here.
4. Run a GPU-backed training (cloud or local GPU) for at least one medium-sized config to validate scaling and reduce training time.

### Where to find outputs
- Logs and samples: `Modelling/experiments/training_runs/` and `Modelling/experiments/samples/`.
- Checkpoints: `Modelling/nanoGPT_project/out-*` (submodule).

### Closing summary
The modelling assignment produced a reproducible prepare → train → sample workflow, artifacts (tokenized dataset, logs, generated samples), and checkpoints in the nanoGPT submodule. Short runs validated the pipeline; a longer CPU run showed further loss reduction but remains compute-limited. The repo contains helper scripts to initialize the submodule and run an end-to-end sanity test. Next steps are to add a small orchestrator, pin package versions, and (optionally) move or share selected checkpoints.

<<<<<<< HEAD:Modelling/README.md
=======

>>>>>>> bce2816 (chore: remove Modelling folder (user requested cleanup)):Modelling - Copy/README.md
