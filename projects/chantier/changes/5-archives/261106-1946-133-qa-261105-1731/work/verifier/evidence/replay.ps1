param([string]$Cli,[string]$Out,[string]$Root)
$ErrorActionPreference='Continue'
$env:PYTHONUTF8='1'
$script:log=New-Object System.Collections.Generic.List[string]
function Run([string]$dir,[string[]]$a){
  $psi=New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName='uv'; $psi.WorkingDirectory=$dir
  $psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true;$psi.UseShellExecute=$false
  $psi.StandardOutputEncoding=[Text.Encoding]::UTF8;$psi.StandardErrorEncoding=[Text.Encoding]::UTF8
  $all=@('run','--script',$Cli)+$a
  $psi.Arguments=($all | % { if($_ -match '[\s"]' -or $_ -eq ''){'"'+($_ -replace '"','\"')+'"'}else{$_} }) -join ' '
  $p=[Diagnostics.Process]::Start($psi)
  $o=$p.StandardOutput.ReadToEnd();$e=$p.StandardError.ReadToEnd();$p.WaitForExit()
  $script:log.Add('$ chantier '+($a -join ' '))
  $txt=($o+$e).TrimEnd(); if($txt){$script:log.Add($txt)}
  $script:log.Add("[exit $($p.ExitCode)]"); $script:log.Add('')
}
function Hd([string]$t){$script:log.Add("## $t")}
function Mkrepo([string]$name){
  $d=Join-Path $Root $name; $o=Join-Path $Root "$name-origin.git"
  git init -q --bare $o 2>$null; git init -q -b main $d 2>$null
  Push-Location $d; git config user.email a@b.c; git config user.name t
  git remote add origin $o; 'x' | Set-Content README.md; git add .; git commit -qm init; git push -q origin main 2>$null; git remote set-head origin main; Pop-Location
  $d
}
function Spec($d,$path,$title){ $f=Join-Path $d $path; New-Item -ItemType Directory -Force $f|Out-Null; "# $title`n" | Set-Content "$f/03-change-spec.md"; "# $title`n" | Set-Content "$f/01-intent.md" }

# ---- repo A
$A=Mkrepo 'A'
Hd 'file twice'
Run $A @('file','Export the report as CSV'); Run $A @('file','Export the report as CSV')
Run $A @('file','Dark mode'); Run $A @('file','Third thing'); Run $A @('file','Fourth')
Hd 'triage'
Run $A @('triage','.agents/changes/1-inbox/dark-mode','--priority','P2')
Run $A @('triage','.agents/changes/2-backlog/P2/dark-mode','--priority','P3')
Run $A @('triage','.agents/changes/2-backlog/P3/dark-mode','--priority','P3')
Run $A @('triage','.agents/changes/3-requests','--priority','P3')
Run $A @('triage','README.md','--priority','P3')
Run $A @('triage','dark','--priority','P3')
Hd 'open 2 CRs'
Spec $A '.agents/changes/1-inbox/export-the-report-as-csv' 'Export the report as CSV'
Spec $A '.agents/changes/1-inbox/third-thing' 'Third thing'
Spec $A '.agents/changes/2-backlog/P3/dark-mode' 'Dark mode'
Run $A @('open','.agents/changes/2-backlog/P3/dark-mode','.agents/changes/1-inbox/export-the-report-as-csv')
Hd 'order drop'
Run $A @('order','drop','CR-101')
Run $A @('status')
Run $A @('order','drop','CR-101')
Run $A @('status')
Run $A @('order','drop','101')
Run $A @('order','drop','101x')
Hd 'cancel then order drop; note on cancelled'
Run $A @('cancel','CR-102')
Run $A @('order','drop','CR-102')
Run $A @('order','note','CR-102','--note','hello')
Run $A @('order','note','CR-101','--note','hello')
Run $A @('order','note','CR-101','--note','hello')
Hd 'rounds and budget'
Run $A @('order','rounds','--note','0')
Run $A @('order','rounds','CR-102','--note','0')
Run $A @('order','rounds','CR-102','--note','3')
Run $A @('order','rounds','CR-102')
Run $A @('order','budget','--note','-5')
Run $A @('order','budget','--note','abc')
Run $A @('order','budget')
Hd 'status and land: applied and pending'
Run $A @('order','qa','--note','check the export')
Run $A @('status')
Run $A @('land')
Hd 'unchanged: close, cost'
Run $A @('close'); Run $A @('close','--yes')
Run $A @('cost')
Run $A @('status')
Hd 'QA folder open'
$qa=Get-ChildItem (Join-Path $A '.agents/changes/1-inbox') -Directory | ? Name -like 'qa-*' | select -First 1
Run $A @('open',".agents/changes/1-inbox/$($qa.Name)")
# ---- repo B: 8 CRs
$B=Mkrepo 'B'
Hd 'open 8 CRs'
$items=@()
1..8 | % { Run $B @('file',"Item number $_ with a fairly long title for the line") | Out-Null }
Get-ChildItem (Join-Path $B '.agents/changes/1-inbox') -Directory | % { Spec $B ".agents/changes/1-inbox/$($_.Name)" $_.Name; $items+=".agents/changes/1-inbox/$($_.Name)" }
Run $B (@('open')+$items)
$last=$script:log[$script:log.Count-3]
# ---- repo C: cost fresh, rounds on cancelled
$C=Mkrepo 'C'
Hd 'cost fresh; rounds on cancelled'
Run $C @('file','One'); Spec $C '.agents/changes/1-inbox/one' 'One'
Run $C @('open','.agents/changes/1-inbox/one')
Run $C @('cost')
Run $C @('cancel','CR-101')
Run $C @('order','rounds','CR-101','--note','4')
$script:log | Set-Content -Encoding utf8 $Out


