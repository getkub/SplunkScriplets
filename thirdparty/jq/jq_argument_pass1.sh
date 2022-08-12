#!/bin/bash

# https://bbs.archlinux.org/viewtopic.php?id=239827

in_port=8000
in_File="../../sampleData/raw/json/sample_array.json"

#jq --arg in_port $in_port --arg out_securityMode "$out_securityMode" 'map(if (.port == $in_port) then .details.securityMode = $out_securityMode else . end )' ${in_File}
jq --arg in_port $in_port 'map(if (.port == 8000) then .details.securityMode = "NA" else . end )' ${in_File}