#!/bin/bash

aws_config_file=~/.aws/config
aws_account_profiles=/tmp/aws_account_profiles

clear 

function tidy_up()
{
  if [ -f ${aws_account_profiles} ];then
     rm -f ${aws_account_profiles}
  fi
}

function switch_profile()
{
  if [ -f "${aws_config_file}" ];then

     # assume role
     aws-azure-login -f
     
     # get profiles
     grep '^\[' ${aws_config_file} |  tr -d '[]' | awk '{print $(NF)}'  > ${aws_account_profiles}

     PS3="Key in Option #: " 
     select aws_account_profile in $(cat ${aws_account_profiles}) exit; do 
        case ${aws_account_profile} in
           exit) echo "exiting"
                 tidy_up
                 return 7 ;;
              *) echo -e "\n Selected $REPLY ===> ${aws_account_profile}"
                 eval $(assume-role ${aws_account_profile})
                 return 7 ;;
        esac
     done
  else
     echo "Please ensure 'aws configure' is completed and profiles are configured"
  fi
}

switch_profile
