#!/bin/bash
#---------------------------------------------------------------------------------#
# Name       = Port Knocking Script                                               #
# Author     = @ihack4falafel                                                     #
# Date       = 9/15/2017                                                          #
# Usage      = chmod +x PortKnokcer.sh && ./PortKnocker.sh                        #
#---------------------------------------------------------------------------------#

# Check user input

if ([ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]); then
  echo -e "\e[33m[*] Usage  : \e[35m$0 <port 1> <port 2> <port 3> <IP Address>\e[33m"
  echo -e "\e[33m[*] Example: \e[35m$0 1 2 3 192.168.199.150                  \e[33m"
  exit 1
fi

# Check nmap

if [ ! type nmap &> /dev/null ]; then
  echo "\e[31m[-]\e[34m Please install nmap and rerun the script.\e[39m"
  exit 0
fi

# Perform port knocking 

echo -e "\e[32m[+]\e[34m Knocking the following ports $1 $2 $3 ...\e[39m"
sleep 3

for port in $1 $2 $3; do nmap --host_timeout 100 --max-retries 0 -PN $4 3 -p $port; done > /dev/null 2>&1

echo -e "\e[32m[+]\e[34m Checking for new open ports with nmap ...\e[39m"
sleep 3

nmap -sT -p- -r -n $4 --open | grep open


