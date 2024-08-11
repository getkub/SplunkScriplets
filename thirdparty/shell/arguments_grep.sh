#!/bin/bash

# echo fruit=apple colour=red
input_args=$@
colourFlag=`echo $input_args | grep colour | awk -F 'colour=' '{print $2}' | awk -F ' ' '{print $1}'`
fruitFlag=`echo $input_args | grep fruit | awk -F 'fruit=' '{print $2}' | awk -F ' ' '{print $1}'`

echo colourFlag=$colourFlag
echo fruitFlag=$fruitFlag


## Better Way
# Set default values for the flags
colourFlag=""
fruitFlag=""

# Loop through all the arguments
for arg in "$@"; do
  case $arg in
    fruit=*)
      fruitFlag="${arg#*=}"
      ;;
    colour=*)
      colourFlag="${arg#*=}"
      ;;
  esac
done

echo "colourFlag=$colourFlag"
echo "fruitFlag=$fruitFlag"
