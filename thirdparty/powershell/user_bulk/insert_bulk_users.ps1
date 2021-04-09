#foreach ($newuser in cat ./users.txt) {
#./NewAdminuser.ps1 -objectname $newuser}

$csv = import-csv "myAdminUserList.csv"
foreach ($item in $csv)
{
"newuser = $($item.user) with password = $($item.password)"

./NewAdminUser.ps1 -objectname $item.user -plainPassword $item.password
}
Write-Host 'The script has completed. Please review the output above for any errors or warnings. Press any key to dismiss.';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');

