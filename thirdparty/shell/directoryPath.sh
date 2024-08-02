# https://stackoverflow.com/questions/242538/unix-shell-script-find-out-which-directory-the-script-file-resides

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
CONFIG_FILE_DIR="$SCRIPTPATH/../../.."

ls -l $CONFIG_FILE_DIR
