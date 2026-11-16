param([string]$Phase, [string]$Cli)
$sp = "C:\Users\gaeta\AppData\Local\Temp\claude\f81ba1603abd10b3\446cff2e-8291-4f73-9ff0-f19c29743e6e\scratchpad"
$ev = "C:\Users\gaeta\Projets\chantier\.agents\changes\4-batch\2-actives\253-baseline-and-legacy\evidence\migration"
$bs = "C:\Users\gaeta\Projets\chantier\.agents\changes\4-batch\2-actives\253-baseline-and-legacy\work\board_state.py"
$ErrorActionPreference = "Continue"
function Run($cwd, $line) {
    Push-Location $cwd
    "`$ $line"
    cmd /c "$line 2>&1"
    "[exit $LASTEXITCODE]"
    Pop-Location
}
$u = "uv run --no-sync --project `"$Cli`""
$o = @()
$o += Run "$sp\chantier-snap" "$u chantier status"
$o += Run "$sp\chantier-snap" "$u chantier cost --batch batch-17"
$o += Run "$sp\chantier-snap" "$u python `"$bs`" chantier . 0"
$o | Out-File "$ev\verify-$Phase-chantier.txt" -Encoding utf8
$o = @()
foreach ($p in Get-ChildItem "$sp\surface-snap\projects" -Directory) {
    $o += "##### $($p.Name)"
    $o += Run "$sp\surface-snap" "$u chantier --project `"$($p.FullName)`" status"
    $o += Run "$sp\surface-snap" "$u python `"$bs`" $($p.Name) `"$($p.FullName)`" 1"
}
$o | Out-File "$ev\verify-$Phase-surface.txt" -Encoding utf8
