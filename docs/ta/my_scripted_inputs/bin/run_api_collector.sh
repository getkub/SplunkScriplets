#!/bin/bash
# Wrapper shell script to run the actual Python script with Splunk's Python interpreter

$SPLUNK_HOME/bin/splunk cmd python $SPLUNK_HOME/etc/apps/my_scripted_inputs/bin/api_collector.py
