$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
$board = Join-Path $projectRoot "hardware\kicad\IPC101.kicad_pcb"
$gerberDir = Join-Path $PSScriptRoot "gerbers"
$kicad = "D:\KiCad\bin\kicad-cli.exe"

New-Item -ItemType Directory -Force -Path $gerberDir | Out-Null

& $kicad pcb drc --exit-code-violations -o (Join-Path $projectRoot "hardware\kicad\IPC101_DRC.rpt") $board
& $kicad pcb export gerbers -o $gerberDir -l "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts" --check-zones $board
& $kicad pcb export drill -o $gerberDir --format excellon --excellon-units mm --excellon-zeros-format decimal --excellon-separate-th --generate-map --map-format pdf --generate-report --report-path (Join-Path $PSScriptRoot "IPC101_RevC_drill_report.txt") $board
& $kicad pcb export pos -o (Join-Path $PSScriptRoot "IPC101_RevC_CPL_all.csv") --side both --format csv --units mm $board
& $kicad pcb export ipcd356 -o (Join-Path $PSScriptRoot "IPC101_RevC.d356") $board
& $kicad pcb export stats -o (Join-Path $PSScriptRoot "IPC101_RevC_board_statistics.txt") $board
& $kicad pcb export pdf --mode-single -o (Join-Path $PSScriptRoot "IPC101_RevC_assembly_reference.pdf") -l "F.Fab,Edge.Cuts" --sketch-pads-on-fab-layers --black-and-white --scale 1 $board

$zip = Join-Path $PSScriptRoot "IPC101_RevC_Gerbers.zip"
$manufacturingFiles = Get-ChildItem $gerberDir -File | Where-Object { $_.Extension -in ".gtl", ".gbl", ".gtp", ".gbp", ".gto", ".gbo", ".gts", ".gbs", ".gm1", ".gbrjob", ".drl" }
Compress-Archive -Force -Path $manufacturingFiles.FullName -DestinationPath $zip

Write-Host "Created $zip"
