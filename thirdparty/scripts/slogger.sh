#!/bin/bash

LOGFILE () {
          SCRIPT_LOG="$1"  
          touch $SCRIPT_LOG
}

SCRIPTENTRY () {
    timeAndDate=`date +"%F %T %Z"`
    script_name=`basename "$0"`
    echo "$FUNCNAME: $script_name" >> $SCRIPT_LOG
}

SCRIPTEXIT () {
    script_name=`basename "$0"`
    echo "$FUNCNAME: $script_name" >> $SCRIPT_LOG
}

ENTRY () {
         local cfn="${FUNCNAME[1]}"
         local tstamp=`date +"%F %T %Z"`
         local msg="> $cfn $FUNCNAME"
    echo -e "$tstamp [DEBUG]\t$msg" >> $SCRIPT_LOG
}

RETURN () {
         local cfn="${FUNCNAME[1]}"
         local tstamp=`date +"%F %T %Z"`
         local msg="< $cfn $FUNCNAME"
    echo -e "$tstamp [DEBUG]\t$msg" >> $SCRIPT_LOG
}

ERROR () {
         local msg="$1"
         local tstamp=`date +"%F %T %Z"`
    echo -e "$tstamp [ERROR]\t$msg" >> $SCRIPT_LOG
}

INFO () {
         local msg="$1"
         local tstamp=`date +"%F %T %Z"`
    echo -e "$tstamp [INFO]\t$msg" >> $SCRIPT_LOG
}

DEBUG () {
         local msg="$1"
         local tstamp=`date +"%F %T %Z"`
    echo -e "$tstamp [DEBUG]\t$msg" >> $SCRIPT_LOG
}
