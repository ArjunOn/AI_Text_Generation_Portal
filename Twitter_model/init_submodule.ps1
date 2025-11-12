<#
init_submodule.ps1

Initialize and update the nanoGPT submodule and show available out-* directories (where checkpoints live).

Usage (from repo root):
  Set-Location A:\Projects\AI_Text_Generation_Portal
  & .\Modelling\init_submodule.ps1
#>

param()

Write-Host "[init_submodule] initializing/updating git submodules"
git submodule update --init --recursive

Write-Host "[init_submodule] listing submodule status"
git submodule status --recursive

Write-Host "[init_submodule] listing out-* directories under Modelling/nanoGPT_project"
if (Test-Path 'Modelling\nanoGPT_project') {
    Get-ChildItem -Path 'Modelling\nanoGPT_project' -Directory -Filter 'out-*' -ErrorAction SilentlyContinue | ForEach-Object { Write-Host $_.FullName }
} else {
    Write-Host 'Modelling/nanoGPT_project not found — did submodule init fail?'
}

Write-Host "[init_submodule] done"
