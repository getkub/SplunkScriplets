' cscript "<scriptname>"

Set fso = CreateObject ("Scripting.FileSystemObject")
Set stdout = fso.GetStandardStream (1)
Set stderr = fso.GetStandardStream (2)

Dim Counter: Counter = 1
Set WshShell = WScript.CreateObject("WScript.Shell")

stdout.WriteLine "Starting for counter: 120mins"

While Counter < 120
  Counter = Counter + 1
  WScript.Sleep 6000
  WshShell.SendKeys "{SCROLLLOCK 2}"
  'stdout.WriteLine "Entry: " & Counter
Wend

Set WshShell = Nothing
