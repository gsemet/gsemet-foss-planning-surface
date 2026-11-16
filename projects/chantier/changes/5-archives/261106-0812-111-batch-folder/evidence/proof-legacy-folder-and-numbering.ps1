$W='C:\Users\gaeta\Projets\chantier.worktrees\batch-folder-CR-111'
$S='C:\Users\gaeta\AppData\Local\Temp\claude\C--Users-gaeta-Projets-chantier\8c6e6ed0-7c80-4a93-90c4-86c238d528b7\scratchpad'
$T="$S\t3"; if(Test-Path $T){Remove-Item -Recurse -Force $T}
New-Item -ItemType Directory $T | Out-Null
git init -q --bare -b main "$T\remote.git"; git clone -q "$T\remote.git" "$T\repo" 2>$null
cd "$T\repo"; git config user.email a@b.c; git config user.name t
"# rules" | Set-Content AGENTS.md; git add .; git commit -qm init; git push -q origin main 2>$null
function Ch { uv run --script "$W\skills\chantier\scripts\cli\chantier.py" @args }
function C { Ch @args; "[exit $LASTEXITCODE]" }
function Prep($t){ $o=@(Ch file $t); $d=(Resolve-Path (($o[0] -replace '^filed ','' -split ';')[0])).Path
 "# $t" | Set-Content "$d\01-intent.md"; "# d" | Set-Content "$d\02-answers.md"; "# $t" | Set-Content "$d\03-change-spec.md"
 $o2=@(Ch triage $d --priority P1); ($o2[0] -replace '^triaged ','' -replace ' \(.*$','') }
$q=Prep "Alpha"
$nb = New-Object Text.UTF8Encoding $false
# legacy landed batch 04-old in 3-requests, old form
$b="$PWD\.agents\changes\3-requests\04-old"; New-Item -ItemType Directory -Force "$b\041-legacy" | Out-Null
[IO.File]::WriteAllText("$b\041-legacy\03-change-spec.md", "# legacy`n", $nb)
$j = '{"id":"04-old","name":"old","version":"0.4.0","created":"2026-10-01T00:00:00Z","status":"landed","host":"claude","mode":"parallel","slots":2,"budget_usd":null,"spent_usd":0.0,"foreman":null,"foreman_epoch":1,"foreman_transcript":null,"stack_agent":null,"heartbeat":null,"settings":{"default_branch":"main","remote":"origin","max_rounds":3},"orders":[],"asks":[],"crs":[{"id":"CR-041","title":"Legacy","kind":"change","status":"merged","order":1,"path":".agents/changes/3-requests/04-old/041-legacy","specification":"03-change-spec.md","round":1,"agent":null,"pr":"https://github.com/x/y/pull/9","branch":"chantier/04-old/cr-041-legacy","worktree":"x","notes":[],"updated":"2026-10-01T00:00:00Z"}],"release":null}'
[IO.File]::WriteAllText("$b\batch.json", $j, $nb)
"== status with a landed legacy folder"; C status
C status --batch 04-old
C status --batch 4
"== open while legacy landed 04-old exists"; C open $q --default-branch main
"== close legacy (by 4, by 04-old)"; C close --batch 4
C close --batch 04-old --yes
Get-ChildItem .agents/changes/3-requests | % Name
"== open: number from folder 04-old before close? now .batch-number:"; if (Test-Path .agents/changes/.batch-number) { Get-Content .agents/changes/.batch-number } else { "(none)" }
C open $q --default-branch main
Get-ChildItem .agents/changes/3-requests | % Name
"== STATUS.json fields"; $sj = Get-Content .agents/changes/3-requests/STATUS.json -Raw | ConvertFrom-Json
$sj.batches[0] | Get-Member -MemberType NoteProperty | % Name
$sj.batches[0].crs[0] | Get-Member -MemberType NoteProperty | % Name
"== .batch-number only (4), nothing else"
Remove-Item -Recurse -Force .agents/changes/3-requests/batch-*
Set-Content .agents/changes/.batch-number "4"
C open $q --default-branch main
