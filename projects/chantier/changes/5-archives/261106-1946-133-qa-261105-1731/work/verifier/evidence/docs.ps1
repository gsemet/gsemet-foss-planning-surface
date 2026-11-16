param([string]$Cli,[string]$Root)
$env:PYTHONUTF8='1'
function Rx { $a=$args; Write-Output ('$ chantier '+($a -join ' ')); & uv run --script $Cli @a 2>&1 | % { "$_" }; Write-Output "[exit $LASTEXITCODE]"; Write-Output '' }
$o="$Root-origin.git"; git init -q --bare $o; git init -q -b main $Root; Set-Location $Root
git config user.email a@b.c; git config user.name t; git remote add origin $o; 'x'|Set-Content README.md; git add .; git commit -qm i; git push -q origin main 2>$null; git remote set-head origin main
Rx file One; $f='.agents/changes/1-inbox/one'; "# s" | Set-Content "$f/03-change-spec.md"; "# One" | Set-Content "$f/01-intent.md"
Rx open $f
Rx close
Rx cost
Rx cancel CR-101
Rx order drop CR-101
Rx order done O-1
Rx land
Rx status
Rx cost
Rx close
Rx status --batch batch-01
Rx cost --batch batch-01

