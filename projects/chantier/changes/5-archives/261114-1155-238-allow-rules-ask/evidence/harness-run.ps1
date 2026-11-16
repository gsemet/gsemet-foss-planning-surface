param($Sp)
$rules = Get-Content "$Sp\rules.json" -Raw | ConvertFrom-Json
$psList = ($rules | % { "'$_'" }) -join ','
$shList = ($rules | % { "'$_'" }) -join ' '
$cases = @(@('1 file absent', $null), @('2 file with other keys', "$Sp\case2.json"), @('3 file already holding some of the rules', "$Sp\case3.json"))
foreach ($shell in 'powershell','posix') {
  foreach ($c in $cases) {
    $h = Join-Path $Sp ("home-$shell-" + $c[0].Substring(0,1)); if (Test-Path $h) { Remove-Item -Recurse -Force $h }
    New-Item -ItemType Directory $h | Out-Null
    $f = Join-Path $h '.claude\settings.json'
    if ($c[1]) { New-Item -ItemType Directory (Split-Path $f) | Out-Null; Copy-Item $c[1] $f }
    $beforeArg = if ($c[1]) { $c[1] } else { '-' }
    "=== $shell, case $($c[0])"
    if ($c[1]) { "before: " + [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($f)).TrimStart([char]0xFEFF) }
    $env:HOME = $h; $env:USERPROFILE = $h
    for ($run = 1; $run -le 2; $run++) {
      if ($shell -eq 'powershell') {
        $line = (Get-Content "$Sp\tpl-ps.txt" -Raw).Trim().Replace('<RULES>', $psList)
        Set-Content "$Sp\line.ps1" $line -Encoding utf8
        powershell -NoProfile -ExecutionPolicy Bypass -File "$Sp\line.ps1"
      } else {
        $line = (Get-Content "$Sp\tpl-sh.txt" -Raw).Trim().Replace('<RULES>', $shList)
        [IO.File]::WriteAllText("$Sp\line.sh", $line + "`n", (New-Object Text.UTF8Encoding $false))
        $h2 = $h.Replace('\','/')
        bash -c "HOME='$h2' sh '$($Sp.Replace('\','/'))/line.sh'"
      }
      "run $run exit=$LASTEXITCODE"
      python "$Sp\verify.py" $f $beforeArg "$Sp\rules.json"
    }
    "after:  " + [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($f))
    "first bytes: " + (([IO.File]::ReadAllBytes($f))[0..2] -join ' ')
  }
}
