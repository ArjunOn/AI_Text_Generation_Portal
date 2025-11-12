<#
run_all.ps1

Purpose: convenience script to (re)prepare dataset, run a short sanity training using the project's venv (if present), and sample outputs.

Usage (from repo root):
  Set-Location A:\Projects\AI_Text_Generation_Portal
  & .\Modelling\nanoGPT_assignment\run_all.ps1

Notes:
- This script defaults to small, fast settings so it's safe to run on CPU for quick validation.
- Adjust $trainArgs to change hyperparameters or iterations.
#>

param()

function Find-ProjectPython {
    $venvPython = Join-Path -Path "Modelling\nanoGPT_project" -ChildPath ".venv\Scripts\python.exe"
    if (Test-Path $venvPython) { return (Resolve-Path $venvPython).Path }
    # fallback to python on PATH
    return "python"
}

Write-Host "[run_all] starting reproducibility flow from repository root"

$projectRoot = (Get-Location).Path
$assignmentDir = Join-Path $projectRoot 'Modelling\nanoGPT_assignment'
$projectVenvPython = Find-ProjectPython

Write-Host "Using Python: $projectVenvPython"

# 1) Prepare dataset
Write-Host "[run_all] running prepare.py to (re)create train.bin / val.bin / meta.pkl"
Set-Location $assignmentDir
& $projectVenvPython .\data\custom_corpus\prepare.py

# 2) Short sanity training (fast) — run from nanoGPT project dir to ensure relative imports work
$trainArgs = @('--device=cpu','--compile=False','--eval_iters=10','--log_interval=1','--block_size=64','--batch_size=12','--n_layer=2','--n_head=2','--n_embd=64','--max_iters=100','--lr_decay_iters=100','--dropout=0.0','--out_dir=out-sanity-short','--always_save_checkpoint=True')

Write-Host "[run_all] running short sanity training (100 iters) — this may take a minute or two on CPU"
Set-Location (Join-Path $projectRoot 'Modelling\nanoGPT_project')
& $projectVenvPython train.py @trainArgs

# 3) Sample using sample_safe.py (will write to out-sanity-short/samples/)
Write-Host "[run_all] sampling from the produced checkpoint using sample_safe.py"
& $projectVenvPython ..\nanoGPT_assignment\sample_safe.py --out_dir=out-sanity-short --device=cpu --num_samples=3 --max_new_tokens=120

Write-Host "[run_all] done — check Modelling/experiments/ (or out-sanity-short/samples/) for generated examples"

# Return to repository root
Set-Location $projectRoot

Write-Host "[run_all] finished"
