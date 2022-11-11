#!/bin/bash

all_envs=('apple' 'banana' 'pear')
for (( i=1; i<=${#all_envs[@]}; i++ ))
do
    echo $i ${all_envs[$i]}

done
