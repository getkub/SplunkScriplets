#! /bin/sh

if [ -r log4sh ]; then
  LOG4SH_CONFIGURATION='log4sh.properties.ex4' . ./log4sh
else
  echo "ERROR: could not load (log4sh)" >&2
  exit 1
fi

# change the default message level from ERROR to INFO
logger_setLevel INFO
threadid=t`date +%s`
logger_setThreadName "$threadid"
sScript=`logger_getFilename`
sHost=`hostname`
sOs=`uname -s`
sUser=`whoami`
logger_info "sScript=$sScript sHost=$sHost sOs=$sOs sUser=$sUser"

# say hello to the world
logger_info "Hello, world!"
logger_error "this is an error"
