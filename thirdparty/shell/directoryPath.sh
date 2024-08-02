SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
CONFIG_FILE_DIR="$SCRIPTPATH/../../.."

ls -l $CONFIG_FILE_DIR
