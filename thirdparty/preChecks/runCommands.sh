#!/bin/sh
# Sample Script for Pre-checks 
# v0.8
# Will create run output of various scripts specified in  $paramList

thisHost=`hostname -s`
outFile="/tmp/preChecks.${thisHost}.log"
paramList="params.csv"
runTime=`date +%F-%T`
runID=`date +%Y%m%d%H%M%S`
if [ -r ${outFile} ]; then
   rm $outFile
fi
touch ${outFile}
chmod 777 ${outFile}
# Read line by line and execute commands
egrep -v "^#" ${paramList} | egrep ',' | while read line
 do 
   group=`echo $line | awk -F "," '{print $1}'` 
   checkType=`echo $line | awk -F "," '{print $2}'` 
   command=`echo $line | tr -d $'\r' | awk -F "," '{print $3}'` 
   command="timeout 1 bash -c '${command}'"
   outVar=`eval $command 2>/dev/null;`
   meta="${runTime} runID=${runID} hostName=${thisHost} testGroup=${group} checkType=${checkType} InputCmd='${command}' Output='${outVar}' "  
   echo $meta >> ${outFile}
 done
