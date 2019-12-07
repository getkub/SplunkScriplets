#!/usr/bin/env bash

SPLUNK_HOME=${SPLUNK_HOME:-/opt/splunk}

set -e
set -u
#set -x

platform="$(uname)"
if [[ "$platform" != 'Linux' ]]; then
    echo "ERROR: This script is only tested on Linux, \`uname\` says this is '$platform'" >&2
    exit 1
fi

function usage()
{
     echo "Usage: $0 [OPTION]"
     echo "Collect stack dumps for splunk support. A good number of samples is in the hundreds, preferably 1000."
     echo
     echo "  -b, --batch      Non-interactive mode, doesn't ask questions."
     echo "  -c, --continuous Collect data continuously, keeping only the latest <samples>"
     echo "                   dump files."
     echo "  -h, --help       Print this message."
     echo "  -i, --interval   Interval between samples, in seconds. Default is 0.5."
     echo "  -o, --outdir     Output directory. Default is '/tmp/splunk'"
     echo "  -p, --pid        PID of process. Default is to use main splunk process if SPLUNK_HOME is set"
     echo "                   or splunk is under '/opt/splunk'"
     echo "  -q, --quiet      Silent mode, output no messages after parameter confirmation (or none at all in batch mode)."
     echo "  -s, --samples    Number of samples -- a good number is in the hundreds. Default 1000."
     echo "  -t, --tool       Valid options are 'gdb' and 'pstack'. The default behavior"
     echo "                   is to prefer pstack only on Redhat-based distros."
}

#
# Handing command-line arguments
#
batch=0
continuous=0
interval=0.5
outdir='/tmp/splunk'
pid=''
quiet=0
if [ -e "$SPLUNK_HOME/var/run/splunk/splunkd.pid" ]; then
    read -r pid < "$SPLUNK_HOME/var/run/splunk/splunkd.pid"
fi
samples=1000
tool='pstack'
while [ "$#" -ne "0" ] ; do
    case "$1" in
        -b|--batch)      batch=1;;
        -c|--continuous) continuous=1;;
        -h|-\?|--help)   usage; exit;;
        --interval=*)    interval=${1#*=};;
        -i|--interval)
            shift
            if [ "$#" -ne "0" ]; then interval="$1"; else interval=''; fi
            ;;
        --outdir=*) outdir=${1#*=};;
        -o|--outdir)
            shift
            if [ "$#" -ne "0" ]; then outdir="$1"; else outdir=''; fi
            ;;
        --pid=*) pid=${1#*=};;
        -p|--pid)
            shift
            if [ "$#" -ne "0" ]; then pid="$1"; else pid=''; fi
            ;;
        -q|--quiet) quiet=1;;
        --samples=*) samples=${1#*=};;
        -s|--samples)
            shift
            if [ "$#" -ne "0" ]; then samples="$1"; else samples=''; fi
            ;;
        --tool=*) tool=${1#*=};;
        -t|--tool)
            shift
            if [ "$#" -ne "0" ]; then tool="$1"; else tool=''; fi
            ;;
        *)
            echo "ERROR: invalid option '$1'" >&2
            exit 1
            ;;
    esac

    if [ "$#" -ne "0" ]; then shift; fi
done

if ! [[ "$interval" =~ ^[0-9]*(|\.[0-9]*)$ && "$interval" =~ [1-9] ]]; then
    echo "ERROR: invalid value for --interval option, '$interval'" >&2
    exit 1
fi

set +e
err="$(mkdir -p "$outdir" 2>&1)"
if [ "$?" -ne "0" ]; then
    echo "ERROR: invalid value for --outdir option, '$outdir': $err" >&2
    exit 1
fi
set -e

if [ -z "$pid" ]; then
    echo "ERROR: pid not specified (SPLUNK_HOME='$SPLUNK_HOME')." >&2
    exit 1
fi
if [[ ! "$pid" =~ ^[1-9][0-9]*$ ]]; then
    echo "ERROR: pid must be a positive integer, not '$pid'." >&2
    exit 1
fi
if [[ ! $samples =~ ^[1-9][0-9]*$ ]]; then
    echo "ERROR: number of samples must be a positive integer, not '$samples'." >&2
    exit 1
fi
case "$tool" in
    gdb)
        try_pstack=0;;
    pstack)
        if [ -e /etc/redhat-release ]; then
            try_pstack=1
        else
            try_pstack=0
        fi
        ;;
    *)
        echo "ERROR: invalid value for --tool option, '$tool'" >&2
        exit 1
esac

#
# Now check what we'll use for stack collection
#
use='gdb'
if (( $try_pstack )); then
    set +e
    if type pstack > /dev/null; then
        use='pstack'
    fi
    set -e
fi
if [ "$use" == "gdb" ]; then
    set +e
    if ! type gdb > /dev/null; then
        echo "ERROR: gdb is unavailable!" >&2
        exit 7
    fi
    set -e
fi

if [ "$batch" -eq "0" ]; then
    echo "Parameters:"
    echo "  SPLUNK_HOME='$SPLUNK_HOME'"
    echo "  --batch=$batch"
    echo "  --continuous=$continuous"
    echo "  --interval=$interval"
    echo "  --outdir='$outdir'"
    echo "  --pid=$pid"
    echo "  --samples=$samples"
    echo "  --tool='$tool' (after evaluating your system tool used will be '$use')"
    echo

    if [[ $samples < 100 ]]; then
        read -p "Number of samples should really be at least 100 -- are you sure you want to continue? (y/n) " choice
    else
        read -p "Do you wish to continue? (y/n) " choice
    fi
    case "$choice" in 
        y|Y ) echo;;
        * )   exit 0;;
    esac
fi

function printout() {
    if [ $quiet -eq 0 ]; then
        echo $@
    fi
}

function printerr() {
    if [ $quiet -eq 0 ]; then
        echo $@ >&2
    fi
}

function timestamp() { date +'%Y-%m-%dT%Hh%Mm%Ss%Nns%z'; }

function collect_proc() {
    set +e
    for d in /proc/$pid /proc/$pid/task/*; do
        lwp=$(basename "$d");
        echo "Thread LWP $lwp";
        cat "$d/$1";
    done
    set -e
}

set +e
type mapfile > /dev/null
set -e
readonly no_mapfile=$?
function lightgrep() {
    local ret=1
    # mapfile+regex for lightweight grepping
    if [ $no_mapfile -eq 0 ]; then
        local data=''
        set +e
        if [ -s "$2" ]; then
            mapfile -t data < "$2" >/dev/null 2>&1
        fi
        if [ -n "$data" ] && [[ "${data[@]}" =~ $1 ]]; then
            ret=0
        fi
        set -e
    else
        if grep -q "$1" "$2" >/dev/null 2>&1; then
            ret=0
        fi
    fi
    return $ret
}

# If the user aborts the script midway through data collection, we still want
# zip up the results.
abort=0
subprocesses=''
function wait_subprocesses_revive_pid() {
    # `wait` won't work because we use setsid for stack collection, so we
    # improvise in a very ugly way
    for proc in $subprocesses; do
        while [ -e /proc/$proc ]; do
            sleep 0.1
        done
    done

    if [ -e /proc/$pid ] && lightgrep "[[:space:]]*State:[[:space:]]*[Tt]" "/proc/$pid/status"; then
        kill -CONT $pid
    fi
}

function archive_on_abort() {
    trap '' SIGINT
    echo "** Trapped CTRL-C. Archiving partial results. Please wait. **"
    wait_subprocesses_revive_pid
    archive
}
trap archive_on_abort INT

# zip up the results
function archive() {
    local outroot="$(dirname "$outdir")"
    local outleaf="$(basename "$outdir")"
    local archive="$outdir.tar.xz"
    tar --remove-files -C "$outroot" -cJf "$archive" "$outleaf"
    printout "Stacks saved in $archive"
}

outdir="$outdir/stacks-${pid}-${HOSTNAME}-$(timestamp)"
mkdir -p "$outdir"

collect_proc "maps" >"$outdir/proc-maps.out" 2>"$outdir/proc-maps.err"

declare -a suffixes
for ((i=0; $i < $samples; i = $continuous ? ($i+1)%$samples : $i+1)); do
    if [ ! -e /proc/$pid ]; then
        printerr $'\n'"Process with pid=$pid no longer available, terminating stack dump collection."
        break;
    fi
    if [ "$batch" -eq "0" ]; then
        printout -n "."
    fi
    suffix="$(timestamp)"
    if [ "${suffixes[$i]+isset}" ]; then
        rm -f "$outdir"/*"${suffixes[$i]}".{out,err}
    fi
    suffixes[$i]=$suffix

    # collect application stack (via pstack or gdb)
    stackdump_fname="$outdir/stack-$use-$suffix"
    if [ "$use" == "gdb" ]; then
        cmd=(gdb -batch -p $pid -n -ex 'thread apply all bt')
    else
        cmd=(pstack $pid)
    fi
    # use setsid to isolate subprocess from signals (like SIGINT)
    setsid "${cmd[@]}" >"$stackdump_fname.out" 2>"$stackdump_fname.err" &
    subprocesses=$!

    # collect /proc/<pid> information for all tasks
    for f in stack status; do
        fname="$outdir/proc-$f-$use-$suffix"
        collect_proc "$f" >$fname.out 2>$fname.err &
    done
    wait

    # wait for application stack program to wrap up
    wait_subprocesses_revive_pid

    if [ -s "$stackdump_fname.err" ]; then
        printout $'\n'"*** Possibly harmless STDERR from \`${cmd[@]}\`:"
        printout "$stackdump_fname.err"
    fi
    if ! lightgrep "Thread.*main" "$stackdump_fname.out" && [ -s "$stackdump_fname.out" ]; then
        printerr $'\n'"ERROR: latest stack dump ($stackdump_fname.out) doesn't contain 'Thread's or 'main()' call! Please try running manually and check output:" >&2
        printerr "  ${cmd[@]}" >&2
        exit 1
    fi

    if [ ! -e /proc/$pid ]; then
        break;
    fi
    sleep $interval
done
printout

archive
