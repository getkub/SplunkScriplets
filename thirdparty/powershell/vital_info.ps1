####################################################################################
#                                                                                  #
#                            Collect important info about Windows system           #
#                                                                                  #
####################################################################################
$c = $env:computername #Use the current computer
#######################################################
#Please adjust the variables below to suit your needs.#
#######################################################

$path = "E:\mylocation\Reading.txt" #Output file path. Directory must exist, file doesn't matter. This is the file to be emailed.
$path2 = "E:\mylocation\services.txt" #Services to be monitored. Shortnames only. File must exist. More info can be found in readme.
$path3 = "E:\mylocation\drives.txt" #Drives to be monitored. Drive letters only. File must exist. More info can be found in readme.
$mailfrom = "test1@myorg.com" #From address on monitoring emails
$mailrec = "test2@test2.co.uk" #Destination to send reports
$smtpserver = "smtp.blah.blah.com" #SMTP server to be used to send final output
$smtpauthu = "user@requiredformat" #Username to authenticate against SMTP server with
$smtpauthp = "passwordinplaintext" # Password to authenticate against SMTP server with


##Hardware Status Gathering##
#This section is used to get#
#information on the hardware#
#status.                    #
#############################

#many kludged together pieces of GoogleCodeTM to gather CPU and RAM info
#$avg = Get-WmiObject win32_processor -computername $c | 
#Measure-Object -property LoadPercentage -Average | 

$avg = Get-Counter '\Processor(*)\% Processor Time' | select -Expand CounterSamples | where{$_.InstanceName -eq '_total'} | select CookedValue | ForEach-Object {$_.cookedvalue}

#Foreach {$_.Average}
$mem = Get-WmiObject win32_operatingsystem -ComputerName $c |
Foreach {"{0:N2}" -f ((($_.TotalVisibleMemorySize - $_.FreePhysicalMemory)*100)/ $_.TotalVisibleMemorySize)}

#Gather disk info. To add more drives edit drives.txt. See readme for more info.
$drvstatus = foreach ($drive in cat $path3) {
get-volume $drive | select-object  DriveLetter, @{Name="GB";Expression={[math]::round($_.Sizeremaining/1GB,2)}} | ft -HideTableHeaders
}

################Service Status gathering##################
#Add service short names to the services.txt file in the #
#script directory. For example"inetsrv" for IIS. You can #
#also change location of the services list by changing   #
#$path2 at the top.                                      #
##########################################################


#Status check for services listed in services.txt ($path2)
$srvstatus= foreach ($services in cat $path2) {
echo $services | Get-Service | Select-Object name, status |ft -HideTableHeaders
}


#TS Session inspection
#Unbelievably complicated way just to get a count of users
$Server = $env:computername

#Initialize $Sessions which will contain all sessions
[System.Collections.ArrayList]$Sessions = New-Object System.Collections.ArrayList($null)

#Get the current sessions on $Server and also format the output
$DirtyOuput = (quser /server:$Server) -replace '\s{2,}', ',' | ConvertFrom-Csv
 
#Go through each session in $DirtyOuput
Foreach ($session in $DirtyOuput) {
  #Initialize a temporary hash where we will store the data
  $tmpHash = @{}
  
  #Check if SESSIONNAME isn't like "console" and isn't like "rdp-tcp*"
  If (($session.sessionname -notlike "console") -AND ($session.sessionname -notlike "rdp-tcp*")) {
    #If the script is in here, the values are shifted and we need to match them correctly
    $tmpHash = @{
	  Username = $session.USERNAME
      SessionName = "" #Session name is empty in this case
      ID = $session.SESSIONNAME
      State = $session.ID
      IdleTime = $session.STATE
      LogonTime = $session."IDLE TIME"
	  Server = $Server
	}
	}Else  {
	  #If the script is in here, it means that the values are correct
	  $tmpHash = @{
	  Username = $session.USERNAME
	  SessionName = $session.SESSIONNAME
	  ID = $session.ID
	  State = $session.STATE
	  IdleTime = $session."IDLE TIME"
	  LogonTime = $session."LOGON TIME"
	  Server = $Server
	  }
	}
	#Add the hash to $Sessions
	$Sessions.Add((New-Object PSObject -Property $tmpHash)) | Out-Null
  }

#Display the sessions and just show Username, ID and Server
$sessions | select Username, ID, $Server | ft -HideTableHeaders | out-string > userlist.txt

#A little cleanup and count total RDP Sessions
$dirtycount= cat .\userlist.txt| measure-object -Line |ft -HideTableHeaders |out-string 
$usercount=$dirtycount.Trim()

#Find Idle Sessions
$idle= $sessions | Select-string 'disc'

######Output Construction######
#This is where the file to be #
#emailed is generated.        #
###############################

#Hardware stats per line
$a = "Avg CPU% " + ($avg.tostring() + "`n" + "Free RAM% " + $mem.tostring()) 

#Write hardware data to a file 
Out-File -FilePath $path -InputObject $a  #-Encoding ASCII

#Add TS metrics and cleanup
$tsinfo= "TS-TotalSess " + ($usercount) + "`n" + "TS-Idle "  + ($idle.count)
echo $tsinfo >> $path

#Nasty way to populate disk info
echo $drvstatus >>$path

#Equally nasty way to append service status to out-file, forcing cleanup later.
echo $srvstatus >> $path

#Remove all blank lines from out-file created by nasty appends
(gc $path) | ? {$_.trim() -ne "" } | set-content $path

#Additional cleanup
$cleanup = get-content -path $path
$final = $cleanup -replace '          ','' -replace 'running','OK' -replace 'stopped','DEAD'
$final | set-content -path $path

###########EMail Wrangling############
#This is where all the juicy info is #
#turned into an email.               #
######################################
$body = get-content -path $path | out-string

$secpasswd = ConvertTo-SecureString "$smtpauthp" -AsPlainText -Force
$mycreds = New-Object System.Management.Automation.PSCredential($smtpauthu, $secpasswd)
## Original line
##Send-MailMessage -from $mailfrom -to $mailrec -subject "Monitoring infomation for $c" -body $body -SmtpServer $smtpserver -usessl -credential $mycreds #replace "-body $body" with "-attachment $path" to send data as attachment instead

## New line - no creds
Send-MailMessage -from $mailfrom -to $mailrec -subject "Monitoring infomation for $c" -body $body -SmtpServer $smtpserver #replace "-body $body" with "-attachment $path" to send data as attachment instead

