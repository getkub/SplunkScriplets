#!/bin/bash
# Replace string 

oldFruit="apple"
newFruit="orange"
oldString="fruit/apple"

if [[ "$oldString" == *"$oldFruit"* ]]
then
    echo $oldString
    newString=${oldString//apple/orange}
    echo $newString
fi 


if [[ "$oldString" == *"$oldFruit"* ]]
then
    echo Var: $oldString
    newString=${oldString//$oldFruit/$newFruit}
    echo Var: $newString
fi 