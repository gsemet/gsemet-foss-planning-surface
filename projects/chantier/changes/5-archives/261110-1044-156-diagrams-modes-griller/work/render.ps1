param([string]$name)
$wt = "C:/Users/gaeta/Projets/chantier.worktrees/batch-09-CR-156/docs"
$r = "C:/Users/gaeta/Projets/chantier/.agents/changes/3-requests/batch-09/156-diagrams-modes-griller/work/render"
$svg = Get-Content "$wt/$name.svg" -Raw -Encoding UTF8
$m = [regex]::Match($svg, 'viewBox="0 0 (\d+) (\d+)"')
$w = $m.Groups[1].Value; $h = $m.Groups[2].Value
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --screenshot="$r/$name.png" --window-size="$w,$h" "file:///$wt/$name.svg" 2>$null | Out-Null
Start-Sleep 1
"$name $w x $h"
