# Export slides to PNG via PowerPoint COM.
# LibreOffice MISP-prints OLE equation / Visio objects (layers overlap);
# PowerPoint's own export renders the true final state.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File _tools\ppt_export.ps1 -Pptx "deck.pptx" -OutDir "out" -Pages "30,60"
# Omit -Pages to export all slides.
param(
  [Parameter(Mandatory=$true)][string]$Pptx,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [string]$Pages = ""
)
$ErrorActionPreference = 'Stop'
$full = (Resolve-Path $Pptx).Path
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }
$outFull = (Resolve-Path $OutDir).Path

$ppt = $null
$pres = $null
try {
  $ppt = New-Object -ComObject PowerPoint.Application
  $pres = $ppt.Presentations.Open($full, $true, $false, $false)
  $total = $pres.Slides.Count
  if ($Pages -eq "") {
    $list = 1..$total
  } else {
    $list = $Pages.Split(',') | ForEach-Object { [int]$_.Trim() }
  }
  $n = 0
  foreach ($i in $list) {
    if ($i -lt 1 -or $i -gt $total) { continue }
    $dest = Join-Path $outFull ("page-{0:D4}.png" -f $i)
    $pres.Slides.Item($i).Export($dest, "PNG", 1600, 900)
    $n++
  }
  Write-Output "EXPORTED $n / $total slides -> $outFull"
} finally {
  if ($pres) { $pres.Close() }
  if ($ppt) { $ppt.Quit() }
  if ($pres) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pres) | Out-Null }
  if ($ppt) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null }
  [GC]::Collect()
}
