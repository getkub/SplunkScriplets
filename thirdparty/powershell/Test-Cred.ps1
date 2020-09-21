# Validate a user credentials are correct.
$thisCreds = Get-Credential
$thisUser = $thisCreds.username
$thisPass = $thisCreds.GetNetworkCredential().password
$Root = "LDAP://" + ([ADSI]'').distinguishedName
$Domain = New-Object System.DirectoryServices.DirectoryEntry($Root,$thisUser,$thisPass)

If ($domain.name -ne $null)

{
    return "Authenticated"
} Else
{
    return "Not authenticated"
}
