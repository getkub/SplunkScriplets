# Powershell script REST method to get information from Splunk

[System.Net.ServicePointManager]::ServerCertificateValidationCAllback = { $True }
$server = 'mysplunkhost'
$my_user = 'splunk_svc'

$url_export = "https://${server}:8089/services/search/jobs/export"
$my_search = 'search `mymacro(param1,parm2)`'

$body = @{
  search = $my_search
  output_mode = "csv"
}

Invoke-RestMethod -Method Post -Uri $url_export -Credential $my_user -Body $body -OutFile output.csv
