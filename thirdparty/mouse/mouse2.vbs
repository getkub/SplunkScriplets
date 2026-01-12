Option Explicit

Dim hours, maxMinutes, Counter
Dim WshShell

' Default to 6 hours
hours = 6

' If parameter is passed, use it
If WScript.Arguments.Count > 0 Then
    If IsNumeric(WScript.Arguments(0)) Then
        hours = CDbl(WScript.Arguments(0))
    End If
End If

maxMinutes = hours * 60
Counter = 0

Set WshShell = WScript.CreateObject("WScript.Shell")

WScript.StdOut.WriteLine "Starting script for " & hours & " hours (" & maxMinutes & " minutes)"

While Counter < maxMinutes
    Counter = Counter + 1
    WScript.Sleep 60000    ' 1 minute
    WshShell.SendKeys "{SCROLLLOCK}"
    'WScript.StdOut.WriteLine "Minute: " & Counter
Wend

WScript.StdOut.WriteLine "Completed " & hours & " hours"

Set WshShell = Nothing
