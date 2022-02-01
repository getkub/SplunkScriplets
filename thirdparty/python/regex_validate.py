# ---------------------------------------------------------------------------------------- #
# Script to load a file and compare against regex
inputParams="absolute_file_name, regex_pattern, HEADER_NO/HEADER_YES, NE/EQ"
inputParamsEg="/tmp/sample.csv  '[\w\-]+' HEADER_NO  NE"
# This script MUST be called by wrapper (as no error checks done in this script)
# ---------------------------------------------------------------------------------------- #
import sys
import re

try:
    input_object_file = sys.argv[1]
    regex_pattern = sys.argv[2]
    include_header = sys.argv[3]
    regex_comparison = sys.argv[4]
except IndexError:
    print ("ERROR: Incorrect input detected. Expected: " + inputParams)
    print ("EXAMPLE: <script_name> " + inputParamsEg)
    sys.exit(1)

pattern = re.compile(regex_pattern)
returnList = []
returnDict = {}
counter = 0
# ------------------------------------------------ #
# IF HEADER_NO, then skip first line
# IF regex_comparison is Not Equal, then do negative check
# ------------------------------------------------ #
with open(input_object_file) as fh:
    if include_header == 'HEADER_NO':
        next(fh)

    for line in fh:
        if regex_comparison == 'NE':
            if not pattern.search(line):
                returnList.append(line)
                counter += 1
        else:
            if pattern.search(line):
                returnList.append(line)
                counter += 1

returnDict['counter'] = counter
returnDict['returnList'] = returnList
print(returnDict)            
