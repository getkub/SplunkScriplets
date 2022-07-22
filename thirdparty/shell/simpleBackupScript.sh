#!/bin/bash

ignore_list=`grep -v '#' ignore_list.txt`
for i in $ignore_list
do
	exclude_chain=${exclude_chain}" --exclude=$i"
done

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
baseDir=~/Documents
backupDir=~/Documents/backup
cd ${baseDir}/mydir/backupScripts

echo "tgz ${baseDir}/rough to ${backupDir}/pers.backup.tgz"
tar $exclude_chain -czf ${backupDir}/pers.backup.tgz -C ${baseDir} mydir
cd $DIR

# ls ${backupDir}
