#!/bin/bash
# Git resolve all current merge conflicts as --ours --theirs --both

die () {
  echo "ERROR: $*. Aborting" >&2
  exit 1
}

args=( )

for arg; do
  case "$arg" in
    --help|-h)
      args+=( -h ) ;;
    --ours|-o)
      args+=( -o ) ;;
    --theirs|-t)
      args+=( -t ) ;;
    --both|-b)
      args+=( -b ) ;;
    *)
      args+=( "$arg" ) ;;
  esac
done

printf 'args before update : '; printf '%q ' "$@"; echo
set -- "${args[@]}"
printf 'args after update  : '; printf '%q ' "$@"; echo

ours=false
theirs=false
both=false

while getopts ":otb" opt; do
    case $opt in
    o ) if [ "$theirs" = true ]; then die "Cannot specify ours and theirs" ;fi
      ours=true ;;
    t ) if [ "$ours" = true ]; then die "Cannot specify ours and theirs" ;fi
      theirs=true ;;
    b ) both=true ;;
    \?) die "Unknown option: -$OPTARG. Abort" ;;
    : ) die "Missing option: -$OPTARG. Abort" ;;
    * ) die "Unimplemented option: -$OPTARG. Abort" ;;
  esac
done

if [ "$ours" == false ] && [ "$theirs" == false ] && [ "$both" == false ]; then
 die "You need to specify --ours, --theirs or --both"
fi

ffiles() { git ls-files -u | cut -f 2 | uniq; }

if [ "$both" = true ]; then
  ffiles | xargs -d '\n' sed -i -e '/<<<<<<</d' -e '/=======/d' -e '/>>>>>>>/d' --
elif [ "$ours" = true ]; then
  ffiles | xargs -d '\n' sed -i -e '/<<<<<<</d' -e '/=======/,/>>>>>>>/d' --
elif [ "$theirs" = true ]; then
  ffiles | xargs -d '\n' sed -i -e '/<<<<<<</,/=======/d' -e '/>>>>>>>/d' --
fi

ffiles | xargs -d '\n' git add --
