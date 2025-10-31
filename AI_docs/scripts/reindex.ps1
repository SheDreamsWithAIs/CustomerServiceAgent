# Reindex Chroma vector store for CustomerServiceAgent
# Usage (from repo root):
#   pwsh -File .\AI_docs\scripts\reindex.ps1
# Optional: ensure OPENAI_API_KEY is available in the process env

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot | Split-Path -Parent
$backendDir = Join-Path $repoRoot 'backend'
$chromaDir = Join-Path $backendDir '.chroma'
$sourceDir = Join-Path $backendDir 'documents_for_agents'

Write-Host "Repo: $repoRoot"
Write-Host "Chroma dir: $chromaDir"
Write-Host "Source dir: $sourceDir"

if (Test-Path $chromaDir) {
  Write-Host "Removing existing Chroma directory..."
  Remove-Item -Recurse -Force $chromaDir
} else {
  Write-Host "No existing Chroma directory found."
}

if (-not (Test-Path $sourceDir)) {
  throw "Source directory not found: $sourceDir"
}

Write-Host "Re-ingesting documents..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw "Python not found on PATH." }

# Run ingestion
Push-Location $backendDir
try {
  python -m app.ingest.ingest_data --source .\documents_for_agents
} finally {
  Pop-Location
}

Write-Host "Reindex complete."
