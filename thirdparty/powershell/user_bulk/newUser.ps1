[CmdletBinding()]
Param(
    [string[]]$ComputerName = $env:COMPUTERNAME,

   # [Parameter(Mandatory=$true)]
   # [ValidateSet("Group","User")]
   # [string]$UserOrGroup,

    [Parameter(Mandatory=$true)]
    [string]$ObjectName
)

#if($UserOrGroup -eq "User") {
    $PasswordForUser = Read-Host -Prompt "Enter a compliant password for the user" -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($PasswordForUser)
    $PlainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR) 
#}

foreach($Computer in $ComputerName) {
   Write-Host "Working on $Computer"
   if(Test-Connection -ComputerName $Computer -count 1 -Quiet) {
        try {
            $CompObject = [ADSI]"WinNT://$Computer"
            $NewObj = $CompObject.Create("User",$ObjectName)
#            if($UserOrGroup -eq "User") {
                $NewObj.SetPassword($PlainPassword)
#            }
            $NewObj.SetInfo()
$AdminGroup = [ADSI]"WinNT://$Computer/Administrators,group"
$User = [ADSI]"WinNT://$Computer/$ObjectName,user"
$AdminGroup.Add($User.Path)
$RDGroup = [ADSI]"WinNT://$Computer/Remote Desktop Users,group"
$User = [ADSI]"WinNT://$Computer/$ObjectName,user"
$RDGroup.Add($User.Path)
            
            Write-Host "User with the name $ObjectName created successfully and added to administrators" -ForegroundColor Green
        } catch {
            Write-Warning "Error occurred while creating the object"
            Write-Verbose "More details : $_"

        }
   } else {
        Write-Warning "$Computer is not online"
   }

}
Write-Host -NoNewLine 'The script has completed. Please review the output above for any errors or warnings. Press any key to dismiss.';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
