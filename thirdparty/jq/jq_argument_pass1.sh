#!/bin/bash

# https://bbs.archlinux.org/viewtopic.php?id=239827

in_port=443
out_clientAuthEnabled=true
in_File="sample_array.json"

jq --arg in_port "$in_port" --arg out_clientAuthEnabled "$out_clientAuthEnabled" 'map(if (.port == $in_port) then .details.clientAuthEnabled = $out_clientAuthEnabled else . end )' ${in_File}
