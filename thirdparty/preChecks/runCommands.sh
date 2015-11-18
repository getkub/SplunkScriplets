#!/bin/sh
# Runs a set of command from CSV file

thisHost=`hostname -s`
outFile=`/tmp/out.${thisHost}.log"
paramList="/tmp/commands.csv"
runID=`date +%Y%m%d%H%M%S`

if [ -r ${outFile} ]; then
  rm $outFile
fi
touch ${outFile}
chmod 777 ${outFile}

# Read line by line and execute
egrep -v "^#" $paramList | egrep ',' | while read line
do
 group=`echo $line | awk -F "," '{print $1}'`
 checks=`echo $line | awk -F "," '{print $2}'`
 cmd=`echo $line | awk -F "," '{print $3}'`
 outVar=`eval $cmd 2>/dev/null`
 info="$runID hostName=${thisHost} testGroup=${group} checks=${checks} cmd=${cmd} out=${outVar}"
 echo `date +%F-%T` $info >> $outFile
done

 
