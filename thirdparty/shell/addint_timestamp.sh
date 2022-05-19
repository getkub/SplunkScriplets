# https://serverfault.com/questions/310098/how-to-add-a-timestamp-to-bash-script-log
./script.sh | while IFS= read -r line; do printf '%s %s\n' "$(date)" "$line"; done
