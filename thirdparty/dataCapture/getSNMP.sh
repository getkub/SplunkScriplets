user=myUser
authprot=SHA
authpass=someKeyKEY
privprot=AES
privpass=someKeyKEYsomeKeyKEY

f5port=161

workdir="/opt/splunk/bin/scripts/snmpGet"
inputConfig="${workdir}/get_snmp.config"
messageID=`date +%s`
interval=25
i=0
runtimeEpoch=0

errorFile="/tmp/snmp_get.error"
if [ ! -f $inputConfig ];
then
   echo "`date +%Y-%m-%d-%H.%M.%S` $inputConfig does NOT exist. Cannot continue" >> ${errorFile}
   exit 0
fi

envTag=`hostname | cut -c 7-9`
siteTag=`hostname | cut -c 5-6`
f5ipList=`grep ^F5 $inputConfig |  grep -i $envTag | grep $siteTag |  awk -F',' '{print $5}'`
# echo "F5ip's : $f5ipList "

# Gets Raw Information about all OID's
for k in `echo ${f5ipList}`
do
 i=0
 results=
 tmpresults=
 tmpFileF5="/tmp/${k}_${messageID}.tmp"
 runtimeEpoch=`date +%s`

 # Test Run to check if there is a timeout. If it timedout, go to next F5
 testRun=
 testRun=$(snmpget -v3 -u $user -a $authprot -A $authpass -x $privprot -X $privpass -l authPriv $k:$f5port 1.3.6.1.4.1.3375.2.1.1.2.1.56.0)
 if [ ! -z "$testRun" ]
 then

   for oid in `grep ^COMPONENT ${inputConfig} | awk -F',' '{print $4}'`
   do
        returnValue=$(snmpget -v3 -u $user -a $authprot -A $authpass -x $privprot -X $privpass -l authPriv $k:$f5port $oid | awk '{ print $4 }' )
        fullinfo=`grep ^COMPONENT ${inputConfig} |grep ${oid}`
        metric=`echo ${fullinfo} | awk -F',' '{print $3}'`
        oidName=`echo ${fullinfo} | awk -F',' '{print $5}'`
        results="$results ${oidName}=$returnValue;"
        echo "${oidName}1=$returnValue" >> ${tmpFileF5}
        (( i++ ))
   done
   echo "RUNTIMEEPOCH1=$runtimeEpoch" >> ${tmpFileF5}
    # logger -p local0.info "MID=F5_SNMP; F5IP=${k}; messageID=${messageID}; LEG=1; RUNTIMEEPOCH1=$runtimeEpoch; $results"
    # echo "MID=F5_SNMP; F5IP=${k}; messageID=${messageID}; LEG=1; RUNTIMEEPOCH1=$runtimeEpoch; $results"
 fi

done

#Second Retrieval after x seconds - No need to give interval as the time difference is around 30 seconds
# sleep $interval

for k in `echo ${f5ipList}`
do
 i=0
 results=
 tmpresults=
 tmpFileF5="/tmp/${k}_${messageID}.tmp"
 runtimeEpoch=`date +%s`

 testRun=
 testRun=$(snmpget -v3 -u $user -a $authprot -A $authpass -x $privprot -X $privpass -l authPriv $k:$f5port 1.3.6.1.4.1.3375.2.1.1.2.1.56.0)
 if [ ! -z "$testRun" ]
 then

   for oid in `grep ^COMPONENT ${inputConfig} | awk -F',' '{print $4}'`
   do
        returnValue=$(snmpget -v3 -u $user -a $authprot -A $authpass -x $privprot -X $privpass -l authPriv $k:$f5port $oid | awk '{ print $4 }' )
        fullinfo=`grep ^COMPONENT ${inputConfig} |grep ${oid}`
        metric=`echo ${fullinfo} | awk -F',' '{print $3}'`
        oidName=`echo ${fullinfo} | awk -F',' '{print $5}'`
        results="$results ${oidName}=$returnValue;"
        echo "${oidName}2=$returnValue" >> ${tmpFileF5}
        (( i++ ))
   done
   echo "RUNTIMEEPOCH2=$runtimeEpoch" >> ${tmpFileF5}
    # logger -p local0.info "MID=F5_SNMP; F5IP=${k}; messageID=${messageID}; LEG=2; RUNTIMEEPOCH2=$runtimeEpoch; $results"
    # echo "MID=F5_SNMP; F5IP=${k}; messageID=${messageID}; LEG=2; RUNTIMEEPOCH2=$runtimeEpoch; $results"
 fi

done

################
# Formula calculation
################

for k in `echo ${f5ipList}`
do
  tmpFileF5="/tmp/${k}_${messageID}.tmp"
  F5_servername=`grep ${k} ${inputConfig} | awk -F',' '{print $6}'`
  F5_servertype=`grep ${k} ${inputConfig} | awk -F',' '{print $3}'`

  if [ -f $tmpFileF5 ]
  then

     for xy in `cat $tmpFileF5`
     do
        eval "$xy"
     done

     Active_Connections_Summary="$sysStatClientCurConns1"
     Active_Connections_client="$sysStatClientCurConns1"
     Active_Connections_server="$sysStatServerCurConns1"
     Active_Connections_ssl_client="$sysClientsslStatCurConns1"
     Active_Connections_ssl_server="$sysServersslStatCurConns1"
     Host_Mem_Usage_bytes="$sysHostMemoryUsed1"
     TMM_Mem_Usage_bytes="$sysStatMemoryUsed1"

     interval=`perl -le 'printf "%.0f", eval"@ARGV"' "($RUNTIMEEPOCH2-$RUNTIMEEPOCH1)"`
     Client_Accepts=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysTcpStatAccepts2-$sysTcpStatAccepts1)/$interval)"`
     Server_Connects=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysStatServerTotConns2-$sysStatServerTotConns1)/$interval)"`
     Client_Connects=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysStatClientTotConns2-$sysStatClientTotConns1)/$interval)"`
     pva_client=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysStatPvaClientTotConns2-$sysStatPvaClientTotConns1)/$interval)"`
     pva_server=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysStatPvaServerTotConns2-$sysStatPvaServerTotConns1)/$interval)"`
     SSL_Client=`perl -le 'printf "%.0f", eval"@ARGV"' "((($sysClientsslStatTotNativeConns2-$sysClientsslStatTotNativeConns1+$sysClientsslStatTotCompatConns2-$sysClientsslStatTotCompatConns1))/$interval)"`
     SSL_Server=`perl -le 'printf "%.0f", eval"@ARGV"' "((($sysServersslStatTotNativeConns2-$sysServersslStatTotNativeConns1+$sysServersslStatTotCompatConns2-$sysServersslStatTotCompatConns1))/$interval)"`
     Server_TcpConnects=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysTcpStatConnects2-$sysTcpStatConnects1)/$interval)"`
     Client_Bits_In=`perl -le 'printf "%.0f", eval"@ARGV"' "((($sysStatClientBytesIn2-$sysStatClientBytesIn1)*8)/$interval)"`
     Client_Bits_Out=`perl -le 'printf "%.0f", eval"@ARGV"' "((($sysStatClientBytesOut2-$sysStatClientBytesOut1)*8)/$interval)"`
     Server_Bits_In=`perl -le 'printf "%.0f", eval"@ARGV"' "((($sysStatServerBytesIn2-$sysStatServerBytesIn1)*8)/$interval)"`
     Server_Bits_Out=`perl -le 'printf "%.0f", eval"@ARGV"' "((($sysStatServerBytesOut2-$sysStatServerBytesOut1)*8)/$interval)"`
     HTTP_Requests=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysStatHttpRequests2-$sysStatHttpRequests1)/$interval)"`
     Hit_Rate=`perl -le 'printf "%.0f", eval"@ARGV"' "($sysHttpStatRamcacheHits1/($sysHttpStatRamcacheHits1+$sysHttpStatRamcacheMisses1)*100)"`
     Byte_Rate=`perl -le 'printf "%.0f", eval"@ARGV"' "($sysHttpStatRamcacheHitBytes1/($sysHttpStatRamcacheHitBytes1+$sysHttpStatRamcacheMissBytes1)*100)"`
     Eviction_Rate=`perl -le 'printf "%.0f", eval"@ARGV"' "($sysHttpStatRamcacheEvictions1/($sysHttpStatRamcacheHits1+$sysHttpStatRamcacheMisses1)*100)"`
     Global_Host_CPU_Usage=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysGlobalHostCpuUser2-$sysGlobalHostCpuUser1+$sysGlobalHostCpuNice2-$sysGlobalHostCpuNice1+$sysGlobalHostCpuSystem2-$sysGlobalHostCpuSystem1)/($sysGlobalHostCpuUser2-$sysGlobalHostCpuUser1+$sysGlobalHostCpuNice2-$sysGlobalHostCpuNice1+$sysGlobalHostCpuIdle2-$sysGlobalHostCpuIdle1+$sysGlobalHostCpuSystem2-$sysGlobalHostCpuSystem1+$sysGlobalHostCpuIrq2-$sysGlobalHostCpuIrq1+$sysGlobalHostCpuSoftirq2-$sysGlobalHostCpuSoftirq1+$sysGlobalHostCpuIowait2-$sysGlobalHostCpuIowait1)*100)"`
     TMM_CPU_Usage=`perl -le 'printf "%.0f", eval"@ARGV"' "(((($sysStatTmTotalCycles2-$sysStatTmTotalCycles1)-($sysStatTmIdleCycles2-$sysStatTmIdleCycles1+$sysStatTmSleepCycles2-$sysStatTmSleepCycles1))/($sysStatTmTotalCycles2-$sysStatTmTotalCycles1))*100)"`
     SSL_TPS=`perl -le 'printf "%.0f", eval"@ARGV"' "(($sysClientsslStatTotCompatConns2-$sysClientsslStatTotCompatConns1+$sysClientsslStatTotNativeConns2-$sysClientsslStatTotNativeConns1)/$interval)"`

     intervalResult="PollIntervalSeconds=$interval; Client_Accepts=$Client_Accepts;  Server_Connects=$Server_Connects;  Client_Connects=$Client_Connects;  pva_client=$pva_client;  pva_server=$pva_server;  SSL_Client=$SSL_Client;  SSL_Server=$SSL_Server;  Server_TcpConnects=$Server_TcpConnects;  Client_Bits_In=$Client_Bits_In;  Client_Bits_Out=$Client_Bits_Out;  Server_Bits_In=$Server_Bits_In;  Server_Bits_Out=$Server_Bits_Out;  HTTP_Requests=$HTTP_Requests;  Hit_Rate=$Hit_Rate;  Byte_Rate=$Byte_Rate;  Eviction_Rate=$Eviction_Rate;  Global_Host_CPU_Usage=$Global_Host_CPU_Usage;  TMM_CPU_Usage=$TMM_CPU_Usage;  SSL_TPS=$SSL_TPS; Active_Connections_Summary=$Active_Connections_Summary; Active_Connections_client=$Active_Connections_client; Active_Connections_server=$Active_Connections_server; Active_Connections_ssl_client=$Active_Connections_ssl_client; Active_Connections_ssl_server=$Active_Connections_ssl_server; Host_Mem_Usage_bytes=$Host_Mem_Usage_bytes; TMM_Mem_Usage_bytes=$TMM_Mem_Usage_bytes; "

      logger -p local0.info "MID=F5_SNMP_INTERVAL; F5IP=${k}; F5SERVERNAME=${F5_servername}; F5SERVERTYPE=${F5_servertype}; messageID=${messageID}; $intervalResult"
     # echo "MID=F5_SNMP_INTERVAL; F5IP=${k}; F5SERVERNAME=${F5_servername}; F5SERVERTYPE=${F5_servertype}; messageID=${messageID}; $intervalResult"
      rm $tmpFileF5

    fi

done
