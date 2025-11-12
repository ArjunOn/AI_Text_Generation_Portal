#!/usr/bin/env bash
# run_all.sh - cross-platform (POSIX) wrapper to prepare dataset, run a short sanity train and sample
# Usage: from repo root: ./Modelling/nanoGPT_assignment/run_all.sh

set -euo pipefail

REPO_ROOT="$(pwd)"
ASSIGN_DIR="$REPO_ROOT/Modelling/nanoGPT_assignment"
PROJECT_DIR="$REPO_ROOT/Modelling/nanoGPT_project"

find_project_python() {
  # Prefer the project's venv python (POSIX path)
  if [ -x "$PROJECT_DIR/.venv/bin/python" ]; then
    echo "$PROJECT_DIR/.venv/bin/python"
    return
  fi
  # Fallback to python on PATH
  if command -v python3 >/dev/null 2>&1; then
    echo "$(command -v python3)"
    return
  fi
  if command -v python >/dev/null 2>&1; then
    echo "$(command -v python)"
    return
  fi
  echo "python not found on PATH" >&2
  return 1
}

PYTHON=$(find_project_python)
echo "[run_all.sh] using python: $PYTHON"

echo "[run_all.sh] step 1/3: preparing dataset"
cd "$ASSIGN_DIR"
"$PYTHON" ./data/custom_corpus/prepare.py

echo "[run_all.sh] step 2/3: running short sanity training (100 iters)"
cd "$PROJECT_DIR"
# small, fast training args (adjust as needed)
TRAIN_ARGS=(--device=cpu --compile=False --eval_iters=10 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=2 --n_head=2 --n_embd=64 --max_iters=100 --lr_decay_iters=100 --dropout=0.0 --out_dir=out-sanity-short --always_save_checkpoint=True)

"$PYTHON" train.py "${TRAIN_ARGS[@]}"

echo "[run_all.sh] step 3/3: sampling using sample_safe.py"
cd "$ASSIGN_DIR"
"$PYTHON" ./sample_safe.py --out_dir=../nanoGPT_project/out-sanity-short --device=cpu --num_samples=3 --max_new_tokens=120

echo "[run_all.sh] done — samples written to Modelling/nanoGPT_project/out-sanity-short/samples/"
