param($minutes = 120)
$myshell = New-Object -com "Wscipt.Shell"

for ($i = 0; $i -lt $minutes; $i++) {
  Start-Sleep -Seconds 60
  $myshell.SendKeys("{SCROLLLOCK 2}")
}
