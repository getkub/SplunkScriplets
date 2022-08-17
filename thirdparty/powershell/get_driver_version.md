```
(Get-WmiObject Win32_PnPSignedDriver| where {$_.DeviceName -eq "Thunderbolt(TM) Controller - 15BF"}).driverversion
```
