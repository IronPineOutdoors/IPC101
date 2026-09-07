$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
$board = Join-Path $projectRoot "hardware\kicad\IPC101.kicad_pcb"
$gerberDir = Join-Path $PSScriptRoot "gerbers"
$kicad = "D:\KiCad\bin\kicad-cli.exe"
$python = Join-Path (Split-Path $kicad) "python.exe"
$maskValidator = Join-Path $PSScriptRoot "validate_solder_mask.py"

function Invoke-KiCad {
    & $kicad @args
    if ($LASTEXITCODE -ne 0) { throw "KiCad failed ($LASTEXITCODE): $args" }
}

& $python $maskValidator --board $board
if ($LASTEXITCODE -ne 0) { throw "Source solder-mask validation failed" }

New-Item -ItemType Directory -Force -Path $gerberDir | Out-Null

Invoke-KiCad pcb drc --exit-code-violations -o (Join-Path $projectRoot "hardware\kicad\IPC101_DRC.rpt") $board
Invoke-KiCad pcb export gerbers -o $gerberDir -l "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts" --check-zones $board
Invoke-KiCad pcb export drill -o $gerberDir --format excellon --excellon-units mm --excellon-zeros-format decimal --excellon-separate-th --generate-map --map-format pdf --generate-report --report-path (Join-Path $PSScriptRoot "IPC101_RevC_drill_report.txt") $board
Invoke-KiCad pcb export pos -o (Join-Path $PSScriptRoot "IPC101_RevC_CPL_all.csv") --side both --format csv --units mm $board
Invoke-KiCad pcb export ipcd356 -o (Join-Path $PSScriptRoot "IPC101_RevC.d356") $board
Invoke-KiCad pcb export stats -o (Join-Path $PSScriptRoot "IPC101_RevC_board_statistics.txt") $board
Invoke-KiCad pcb export pdf --mode-single -o (Join-Path $PSScriptRoot "IPC101_RevC_assembly_reference.pdf") -l "F.Fab,Edge.Cuts" --sketch-pads-on-fab-layers --black-and-white --scale 1 $board

$zip = Join-Path $PSScriptRoot "IPC101_RevC_MaskFix_Gerbers.zip"
$manufacturingFiles = Get-ChildItem $gerberDir -File | Where-Object { $_.Extension -in ".gtl", ".gbl", ".gtp", ".gbp", ".gto", ".gbo", ".gts", ".gbs", ".gm1", ".gbrjob", ".drl" }
& $python $maskValidator --board $board --gerbers $gerberDir
if ($LASTEXITCODE -ne 0) { throw "Gerber solder-mask validation failed" }
Compress-Archive -Force -Path $manufacturingFiles.FullName -DestinationPath $zip

& $python $maskValidator --board $board --gerbers $gerberDir --zip $zip
if ($LASTEXITCODE -ne 0) { throw "Archived solder-mask validation failed" }

Write-Host "Created $zip"
