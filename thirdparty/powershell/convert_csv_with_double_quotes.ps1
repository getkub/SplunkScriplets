Import-Csv ".\SourceFile.csv" | Export-Csv ".\DestinationFile.csv" -NoTypeInformation



# To Find duplicates & non-duplicates
myfile="blah.csv"
Import-Csv $myfile | group-Object -Property device_ip| Where{$_.Count -gt 1} | Foreach-Object {$_.Group} | Export-csv -Path yes_duplicates.csv -NoTypeInformation
Import-Csv $myfile | group-Object -Property device_ip| Where{$_.Count -lt 2} | Foreach-Object {$_.Group} | Export-csv -Path non_duplicates.csv -NoTypeInformation

# Then in notepad++ (for duplicates)
(.+,.+)\r\n.+,.+  => \1
