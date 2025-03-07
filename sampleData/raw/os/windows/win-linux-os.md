# Log Types Comparison: Windows Server 2012, Red Hat 7.9, Oracle Linux, and Kubernetes

## Windows Server 2012 Log Types

| Log Type | Sample Data |
|----------|-------------|
| **Application Log** | `Information 8/24/2024 10:15:32 AM Application 1000 None Microsoft Office Word has successfully started.` |
| **System Log** | `Warning 8/24/2024 9:02:14 AM System 1021 Disk The driver detected a controller error on \Device\Harddisk1\DR1.` |
| **Security Log** | `Audit Success 8/24/2024 8:45:22 AM Security 4624 None An account was successfully logged on. Subject: Security ID: S-1-5-18 Account Name: WINSERVER$ Account Domain: WORKGROUP Logon ID: 0x3e7 Logon Type: 2` |
| **Setup Log** | `Information 8/23/2024 6:30:45 PM Setup 11 None Windows update successfully installed updates: KB5034289.` |
| **Directory Service** | `Information 8/24/2024 7:00:12 AM Directory Service 1314 None Active Directory Domain Services started successfully.` |
| **DNS Server** | `Error 8/24/2024 2:15:02 PM DNS Server 4015 None The DNS server was unable to complete directory service enumeration of zone domain.local. The extended error debug information (which may be empty) is "". The event data contains the error.` |
| **File Replication Service** | `Information 8/24/2024 3:45:29 AM File Replication Service 13516 None The File Replication Service is no longer preventing the computer WINSERVER from becoming a domain controller.` |
| **IIS Logs** | `172.16.8.25 - admin [24/Aug/2024:10:55:36 -0500] "GET /default.aspx HTTP/1.1" 200 2048 "http://intranet/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"` |
| **Task Scheduler** | `Information 8/24/2024 4:00:00 AM TaskScheduler 102 None Task Scheduler successfully completed task "\Microsoft\Windows\Maintenance\WinSAT" , instance "{c6a1ef0c-d4df-4ac1-9cfa-2a5d84d1ca7c}" , action "C:\Windows\system32\WinSAT.exe" with return code 0.` |
| **Windows Defender** | `Information 8/24/2024 12:30:45 PM Windows Defender 1001 None Windows Defender scan completed successfully. No threats detected.` |
| **Windows Update** | `Information 8/24/2024 3:15:22 AM Windows Update Agent 19 None Installation Successful: Windows successfully installed the following update: Security Update for Windows (KB5034765)` |
| **PowerShell** | `Information 8/24/2024 11:22:31 AM PowerShell 600 None Provider "Variable" is Started. Details: ProviderName=Variable` |
| **Windows Firewall** | `Information 8/24/2024 8:30:18 AM Windows Firewall 2004 None A rule has been added to the Windows Defender Firewall exception list. Rule Name: File and Printer Sharing (Echo Request - ICMPv4-In)` |
| **Event Viewer Custom Views** | `Warning 8/24/2024 10:45:02 AM Kernel-PnP 219 None The driver \Driver\WUDFRd failed to load for the device ROOT\WPD\0000.` |

## Red Hat 7.9 Log Types

| Log Type | Sample Data |
|----------|-------------|
| **/var/log/messages** | `Aug 24 10:35:45 rhserver01 systemd: Started System Logging Service.` |
| **/var/log/secure** | `Aug 24 09:45:22 rhserver01 sshd[12345]: Accepted publickey for admin from 192.168.1.105 port 52413 ssh2: RSA SHA256:KMn3ihyHJ7yBvK4Vjkd99LwBzXc/QUlxV50pj2lIBQ` |
| **/var/log/boot.log** | `[ OK ] Started Show Plymouth Boot Screen.` |
| **/var/log/dmesg** | `[    0.000000] Initializing cgroup subsys cpuset` |
| **/var/log/audit/audit.log** | `type=USER_AUTH msg=audit(1629807922.796:4956): pid=17254 uid=0 auid=1000 ses=98 subj=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 msg='op=PAM:authentication grantors=pam_unix acct="root" exe="/usr/bin/sudo" hostname=? addr=? terminal=/dev/pts/0 res=success'` |
| **/var/log/cron** | `Aug 24 04:01:01 rhserver01 CROND[12543]: (root) CMD (/usr/lib64/sa/sa1 1 1)` |
| **/var/log/maillog** | `Aug 24 08:23:45 rhserver01 postfix/smtpd[12678]: connect from mail.example.com[192.168.10.15]` |
| **/var/log/httpd/access_log** | `192.168.1.105 - - [24/Aug/2024:11:42:33 -0400] "GET /index.html HTTP/1.1" 200 2348 "http://intranet.example.com/" "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"` |
| **/var/log/httpd/error_log** | `[Sun Aug 24 11:38:22 2024] [error] [client 192.168.1.105] PHP Warning: include(/var/www/includes/config.php): failed to open stream: No such file or directory in /var/www/html/index.php on line 25` |
| **/var/log/yum.log** | `Aug 24 07:15:45 Updated: kernel-3.10.0-1160.71.1.el7.x86_64` |
| **/var/log/mariadb/mariadb.log** | `2024-08-24 12:34:56 139745356540672 [Note] InnoDB: Database was not shutdown normally!` |
| **/var/log/cups/error_log** | `E [24/Aug/2024:13:45:22 -0400] [Job 42] Unable to open print file: No such file or directory` |
| **/var/log/samba/log.smbd** | `[2024/08/24 14:25:30.456789,  0] ../source3/smbd/service.c:575(make_connection_snum) rhserver01 (ipv4:192.168.1.105:49322) connect to service SharedDocs initially as user nobody (uid=99, gid=99)` |
| **/var/log/lastlog** | (Binary file showing last login information for users) |
| **/var/log/wtmp** | (Binary file recording logins) |
| **/var/log/btmp** | (Binary file recording failed login attempts) |
| **/var/log/firewalld** | `2024-08-24 08:30:22 ERROR: COMMAND_FAILED: '/usr/sbin/iptables -w2 -t filter -A INPUT_direct -p icmp -j ACCEPT' failed: iptables: No chain/target/match by that name.` |
| **journalctl** | `Aug 24 15:45:30 rhserver01 systemd[1]: Starting Journal Service...` |

## Oracle Linux (Latest) Log Types

| Log Type | Sample Data |
|----------|-------------|
| **/var/log/messages** | `Aug 24 10:12:33 oraclelinux systemd: Starting System Logging Service...` |
| **/var/log/secure** | `Aug 24 11:35:22 oraclelinux sshd[2345]: Accepted password for oracle from 10.0.0.25 port 52413 ssh2` |
| **/var/log/boot.log** | `[ OK ] Started Show Plymouth Boot Screen.` |
| **/var/log/dmesg** | `[    0.000000] Linux version 5.4.17-2136.314.6.el8uek.x86_64` |
| **/var/log/audit/audit.log** | `type=USER_LOGIN msg=audit(1629807922.796:4956): pid=17254 uid=0 auid=1000 ses=98 subj=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 msg='op=login id=oracle res=success'` |
| **/var/log/cron** | `Aug 24 04:01:01 oraclelinux CROND[12543]: (oracle) CMD (/home/oracle/scripts/backup.sh)` |
| **/var/log/maillog** | `Aug 24 08:23:45 oraclelinux postfix/smtpd[12678]: connect from mail.example.com[192.168.10.15]` |
| **/var/log/httpd/access_log** | `10.0.0.25 - - [24/Aug/2024:11:42:33 -0400] "GET /apex/f?p=4550 HTTP/1.1" 200 24815 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"` |
| **/var/log/httpd/error_log** | `[Sun Aug 24 11:38:22 2024] [error] [client 10.0.0.25] ORA-12505: TNS:listener does not currently know of SID given in connect descriptor` |
| **/var/log/yum.log** | `Aug 24 07:15:45 Updated: oraclelinux-release-el8-1.0-13.el8.x86_64` |
| **/var/log/oracle/rdbms/alert_ORCL.log** | `Sun Aug 24 13:00:35 2024 Starting ORACLE instance (normal)` |
| **/var/log/oracle/rdbms/listener.log** | `24-AUG-2024 13:01:25 * (CONNECT_DATA=(SID=ORCL)(CID=(PROGRAM=sqlplus)(HOST=oraclelinux)(USER=oracle))) * (ADDRESS=(PROTOCOL=tcp)(HOST=10.0.0.25)(PORT=52435)) * establish * ORCL * 0` |
| **/var/log/oracle/rdbms/trace/ORCL_ora_12345.trc** | `*** 2024-08-24 13:05:44.261 ORCL(3):  ksedmp: internal or fatal error ORA-00600: internal error code, arguments: [kddummy_blkchk], [0x8695E008], [], [], [], [], [], [], [], [], [], []` |
| **/var/log/oracle/diag/rdbms/ORCL/ORCL/trace/alert_ORCL.log** | `Sun Aug 24 14:12:33 2024 Database mounted in Exclusive Mode` |
| **/var/log/cups/error_log** | `E [24/Aug/2024:13:45:22 -0400] [Job 42] Unable to open print file: No such file or directory` |
| **/var/log/lastlog** | (Binary file showing last login information for users) |
| **/var/log/wtmp** | (Binary file recording logins) |
| **/var/log/btmp** | (Binary file recording failed login attempts) |
| **/var/log/firewalld** | `2024-08-24 08:30:22 ERROR: COMMAND_FAILED: '/usr/sbin/iptables -w2 -t filter -A INPUT_direct -p tcp --dport 1521 -j ACCEPT' failed: iptables: No chain/target/match by that name.` |
| **journalctl** | `Aug 24 15:45:30 oraclelinux systemd[1]: Starting Oracle Database Service...` |
| **/var/log/ovm-manager-3/ovm-console.log** | `2024-08-24 09:12:33,456 INFO [main] Starting Oracle VM Manager Console version 3.4.6.2102` |
| **/var/log/ksplice/uptrack.log** | `2024-08-24 06:00:01 INFO: Checking for available updates` |

## Kubernetes Log Types

| Log Type | Sample Data |
|----------|-------------|
| **Pod Logs** | `2024-08-24T10:35:45.123456Z INFO Server started successfully on port 8080` |
| **Container Logs** | `2024-08-24T11:20:33.456789Z ERROR Failed to connect to database: Connection refused` |
| **API Server Logs** | `I0824 09:45:22.345678 12345 request.go:1154] Throttling request took 1.035s, request: GET:/api/v1/namespaces/kube-system/pods` |
| **Controller Manager Logs** | `I0824 10:15:35.123456 12345 deployment_controller.go:518] Started deployment controller` |
| **Scheduler Logs** | `I0824 12:10:22.123456 12345 scheduler.go:618] Attempting to schedule pod: default/nginx-deployment-5c689d88bb-abc12` |
| **kubelet Logs** | `I0824 13:05:45.123456 12345 kubelet.go:1926] SyncLoop (ADD, "api"): "nginx-deployment-5c689d88bb-abc12_default(f3d52441-1a6d-11e9-8a12-0a58ac1f08f6)"` |
| **kube-proxy Logs** | `I0824 14:22:33.123456 12345 proxier.go:799] Syncing endpoints for service "kube-system/kube-dns:dns-tcp" at [2024-08-24 14:22:33 +0000 UTC]` |
| **etcd Logs** | `2024-08-24T15:25:45.123456Z info etcdserver/api/v3rpc/lease.go:65 lease keepalive received {"remote-ip": "10.244.0.5:59840", "lease-id": 4513043349990745353, "lease-ttl": 580}` |
| **Event Logs** | `Warning FailedMount 3m ago kubelet, node1 MountVolume.SetUp failed for volume "config-volume" : configmap "nginx-config" not found` |
| **Audit Logs** | `{"kind":"Event","apiVersion":"audit.k8s.io/v1","level":"Metadata","auditID":"6c96c0a5-3b6f-4add-a3ce-a9b500c8584c","stage":"ResponseComplete","requestURI":"/api/v1/namespaces/default/pods","verb":"list","user":{"username":"system:serviceaccount:kube-system:deployment-controller","groups":["system:serviceaccounts","system:serviceaccounts:kube-system","system:authenticated"]},"sourceIPs":["10.244.0.1"],"userAgent":"kube-controller-manager/v1.24.0","objectRef":{"resource":"pods","namespace":"default","apiVersion":"v1"},"responseStatus":{"metadata":{},"code":200},"requestReceivedTimestamp":"2024-08-24T10:25:30.123456Z","stageTimestamp":"2024-08-24T10:25:30.234567Z","annotations":{"authorization.k8s.io/decision":"allow","authorization.k8s.io/reason":"RBAC: allowed by ClusterRoleBinding \"system:kube-controller-manager\" of ClusterRole \"system:kube-controller-manager\" to User \"system:serviceaccount:kube-system:deployment-controller\""}}` |
| **Ingress Controller Logs** | `10.244.0.5 - - [24/Aug/2024:16:30:15 +0000] "GET /api/v1/products HTTP/1.1" 200 4215 "https://api.example.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" 123 0.035 [default-web-app-80] 10.244.2.5:8080 4215 0.033 200 abf93bfafec0db88c29a9671c97c7763` |
| **Prometheus Logs** | `level=info ts=2024-08-24T17:35:22.123Z caller=head.go:644 msg="Head GC completed" duration=12.345ms` |
| **Helm Logs** | `2024-08-24T18:10:45.123Z [helm.sh/3.9.0] WARN: Kubernetes configuration file is group-readable.` |
| **CSI Driver Logs** | `I0824 19:22:33.123456 12345 csi_driver.go:123] Successfully provisioned volume pvc-f3d52441-1a6d-11e9-8a12-0a58ac1f08f6` |
| **Custom Resource Controller Logs** | `2024-08-24T20:15:35.123Z INFO Successfully reconciled CustomResource example-cr in namespace default` |
| **Service Mesh Logs (Istio)** | `2024-08-24T21:05:22.123456Z info envoy config/filter/http/rbac/v2:5] shadow denied check for rule solo string: none to principal: request[path:/api/v1/products?id=123 path_safe:/api/v1/products?id=123]` |
| **Kubernetes Dashboard Logs** | `2024-08-24T22:30:45Z [INFO] Getting list of all deployments in namespace default` |
| **Persistent Volume Logs** | `I0824 23:15:22.123456 12345 pv_controller.go:500] Provisioning volume for claim "default/data-pvc" succeeded` |
