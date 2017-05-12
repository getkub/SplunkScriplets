
$LogTime = Get-Date -Format "yyyy-MM-ddThh:mm:sszzz"

# ------------------------------------------------------------
# This will insert Data Directly into Windows EventLog
# ------------------------------------------------------------

$LogName="Application"
$Source="getkub_app"
$EntryType="Error"
$EventId="7032"
$Message="Sample Message winEventLogGen " + "DateTimeSource:" + $LogTime + "EventSourceId:" + $EventId

    Try
    {
	    # Use New-EventLog if you instantiating for first Time
    	#New-EventLog -LogName $LogName -Source $Source
		Write-EventLog -LogName $LogName -Source $Source -EntryType $EntryType -Message $Message -EventId $EventId
    }
    Catch
    {
    	$ErrorMessage = $_.Exception.Message
    	$FailedItem = $_.Exception.ItemName
    	Write-Host "Error occured for Item Name:" $FailedItem "::" "Error Message:" $ErrorMessage
    	Break
    }
# Now go back to original where you started running the script
Set-Location -Path $scriptDir
