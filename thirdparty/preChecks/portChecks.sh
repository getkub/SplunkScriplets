#!/bin/sh
# Sample Script Testing Ports v0.4
# Author KK, ECS
# Script goes through all port sets and do a huge matrix test 

#Please run this script from /tmp/

thisHost=`hostname -s`
outFile="/tmp/portChecks.${thisHost}.log"
paramList="ports.list"
full_serverList="server.mgmt.list"
runTime=`date +%F-%T`
runID=`date +%Y%m%d%H%M%S`
group="PortTest"
if [ -r ${outFile} ]; then
   rm $outFile
fi
touch ${outFile}
chmod 777 ${outFile}

envment=`echo ${thisHost} | cut -c 1`
ssite=`echo ${thisHost} | rev | cut -c 3`
if [ $envment == "t" ]; then
    site="TEST"
   	grep -i TEST ${full_serverList} >> test.mgmt.list
	serverList=test.mgmt.list
elif [ $ssite == "d" ]; then 
    site="DEV"
   	grep -i DEV ${full_serverList} >> dev.mgmt.list
	serverList=dev.mgmt.list
elif [ $ssite == "n" ]; then 
    site="SITE2"
   	grep -i ACT ${full_serverList} | grep -i W0 >> secondary.mgmt.list	
	serverList=secondary.mgmt.list
elif [ $ssite == "s" ]; then
    site="SITE1"
   	grep -i PASS ${full_serverList} | grep -i S0 >> primary.mgmt.list	
	serverList=primary.mgmt.list
else
    site="NA"
fi

echo "Running ports Test for $serverList "
# Read line by line and execute commands
items="fwd sh ind cm dep"
egrep -v "^#" ${paramList} | egrep ',' | while read line
 do 
   port=`echo $line | awk -F "," '{print $1}'` 
   desc=`echo $line | awk -F "," '{print $2}'` 
   fwd=`echo $line | awk -F "," '{print $3}'` 
   sh=`echo $line | awk -F "," '{print $4}'` 
   ind=`echo $line | awk -F "," '{print $5}'` 
   clm=`echo $line | awk -F "," '{print $6}'` 
   aux=`echo $line | tr -d $'\r' | awk -F "," '{print $7}'`
   for item in `echo $items`
   do
		itemValue=`eval echo '$'$item`   # This will evaluate value of item to itemValue
        if [ $itemValue == "Yes" ]; then
        	checkType=${item}_${port}
        	searchStr=${item}${ssite}
             egrep -v "^#" ${serverList} | egrep ',' | egrep -i "${searchStr}"| while read ser
             do
             	destIP=`echo $ser | awk -F "," '{print $2}'`
				destName=`echo $ser | awk -F "," '{print $1}'`
             	command="timeout 1 bash -c 'echo 1>/dev/null 2>/dev/null < /dev/tcp/${destIP}/${port}'"
             	outVar=`eval $command 2>/dev/null; echo $?`
				meta="${runTime} runID=${runID} hostName=${thisHost} testGroup=${group} checkType=${checkType} destination=${destName} InputCmd='${command}' Output='${outVar}' " 
                echo $meta	>> ${outFile}			
             done
        fi
	done
 done
 rm ${serverList}  2>/dev/null
