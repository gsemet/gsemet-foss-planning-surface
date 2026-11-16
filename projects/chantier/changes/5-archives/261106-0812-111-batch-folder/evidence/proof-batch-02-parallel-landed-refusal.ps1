$W='C:\Users\gaeta\Projets\chantier.worktrees\batch-folder-CR-111'
$T='C:\Users\gaeta\AppData\Local\Temp\claude\C--Users-gaeta-Projets-chantier\8c6e6ed0-7c80-4a93-90c4-86c238d528b7\scratchpad\t1'
cd "$T\repo"
function Ch { uv run --script "$W\skills\chantier\scripts\cli\chantier.py" @args }
function C { Ch @args; "[exit $LASTEXITCODE]" }
function Prep($t){ $o=@(Ch file $t); $d=(Resolve-Path (($o[0] -replace '^filed ','' -split ';')[0])).Path
 "# $t" | Set-Content "$d\01-intent.md"; "# d" | Set-Content "$d\02-answers.md"; "# $t" | Set-Content "$d\03-change-spec.md"
 $o2=@(Ch triage $d --priority P1); ($o2[0] -replace '^triaged ','' -replace ' \(.*$','') }
git -C . status --short | out-null
# clean the stray inbox item
Remove-Item -Recurse -Force .agents/changes/1-inbox/delta-four -ErrorAction SilentlyContinue
$q=Prep "Delta four"; $r=Prep "Echo five"
"== open again (expect batch-02, count continues after close)"; C open $q --parallel --slots 2 --default-branch main
Get-ChildItem .agents/changes/3-requests | % Name; Get-Content .agents/changes/.batch-number
C status | select -first 2
Select-String '"mode"|"slots"|"branch"|"id"' .agents/changes/3-requests/batch-02/batch.json | % Line | select -first 5
C foreman set f2 --epoch 1; C take CR-104 --epoch 1 | select -first 1
C cancel CR-104 | select -last 2
"cancelled; land"; C land --epoch 1
Get-Content .agents/changes/3-requests/batch-02/batch.json | Select-String '"status"' | select -first 1
"== open while landed"; C open $r --default-branch main
"== STATUS.json top"; Get-Content .agents/changes/3-requests/STATUS.json | select -first 14
