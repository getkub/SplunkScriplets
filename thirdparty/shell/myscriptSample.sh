#!/bin/bash

my_dir="$(dirname "$0")"

. "$my_dir/slogger.sh"

thisLogFile=/tmp/SystemOut1.log
LOGFILE "$thisLogFile"

echo SCRIPTENTRY
SCRIPTENTRY
updateUserDetails() {
	echo ENTRY
    ENTRY
	echo DEBUG
    DEBUG "Username: $1, Key: $2"
 	echo INFO
    INFO "User details updated for $1"
	echo RETURN
    RETURN
}

echo INFO
INFO "Updating user details..."
echo updateUserDetails
updateUserDetails "testUser" "12345"

rc=2

if [ ! "$rc" = "0" ]
then
    ERROR "Failed to update user details. RC=$rc"
fi
SCRIPTEXIT
