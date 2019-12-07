#!/usr/bin/env bash


# $SPLUNK_HOME/bin/scripts/jemalloc-search-process.sh
#
# Write the following to $SPLUNK_HOME/system/local/limits.conf
# [search]
# search_process_mode = debug $SPLUNK_HOME/bin/scripts/jemalloc-search-process.sh

# Stop splunk and start it up with jemalloc dumps enabled:
#   $SPLUNK_HOME/bin/splunk stop
#   MALLOC_CONF="prof:true,prof_accum:true,prof_leak:true,lg_prof_interval:34,prof_prefix:/tmp/mem" $SPLUNK_HOME/bin/splunk start

readonly sid_marker="RMD5eddd0618b168fff8"

# find the search id
for arg in "$@"; do
  # --id=<sid>
  if [[ "$arg" =~ --id=(.*) ]]; then
    id=${BASH_REMATCH[1]}
  fi
done

# setup script for testing when no arguments given
if [ $# -eq 0 ]; then
    id=$sid_marker
    set -- sleep 15
    echo "Test will take 15s, please check '$SPLUNK_HOME/var/run/splunk/dispatch/$id' for resulting data"
fi

if ! [[ "$id" =~ $sid_marker ]]; then
    exec "$@"
fi

readonly logcfg="$SPLUNK_HOME/etc/log-searchprocess-local.cfg"
readonly logbkp="$logcfg.bkp"
if ! [ -e "$logcfg" ]; then
    touch "$logbkp"
elif ! [ -e "$logbkp" ]; then
    mv "$logcfg" "$logbkp"
fi
echo 'rootCategory=DEBUG,searchprocessAppender
appender.searchprocessAppender.maxFileSize=50000000
appender.searchprocessAppender.maxBackupIndex=5' > "$logcfg"


readonly dispatch="$SPLUNK_HOME/var/run/splunk/dispatch/$id"
readonly jemalloc="$dispatch/jemalloc"
mkdir -p "$jemalloc"
echo "$@" > "$dispatch/splunk.cmd"
:>$dispatch/save

MALLOC_CONF="prof:true,prof_accum:true,prof_leak:true,lg_prof_interval:28,prof_prefix:$jemalloc/mem" "$@" &
readonly pid=$!

"$SPLUNK_HOME/bin/scripts/collect-stacks.sh" -b -c -o "$dispatch" -s 10000 -p $pid -q &

# wait for search.log to come up
for i in {1..30}; do
    if [ -e "$dispatch/search.log" ]; then
        break
    fi
    sleep 1
done
# restore log configs
if [ -e "$logbkp" ]; then
    mv "$logbkp" "$logcfg"
fi

wait $pid
readonly ret=$?
wait

exit $ret
