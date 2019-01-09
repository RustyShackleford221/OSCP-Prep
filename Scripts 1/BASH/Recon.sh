#!/bin/bash
#---------------------------------------------------------------------------------#
# Name       = Quick n' Dirty Recon Script                                        #
# Author     = @ihack4falafel                                                     #
# Date       = 9/12/2017                                                          #
# Usage      = chmod +x Recon.sh && ./Recon.sh <IP Address>                       #
#---------------------------------------------------------------------------------#



# check for IP argument

if [ -z "$1" ]; then
  echo -e "\e[35m[*] Usage: \e[36m$0 <IP Address>"
  echo -e "\e[39m"
  exit 1
fi

# check if packages are installed

if [ ! type nmap &> /dev/null ]; then
  echo "                                            "
  echo "Please install nmap and rerun the script."
  echo "                                            "
  exit 0
fi

if [ ! type nikto &> /dev/null ]; then
  echo "                                            "
  echo "Please install nikto and rerun the script."
  echo "                                            "
  exit 0
fi

if [ ! type dirb &> /dev/null ]; then
  echo "                                            "
  echo "Please install dirb and rerun the script."
  echo "                                            "
  exit 0
fi

if [ ! locate enum4linux &> /dev/null ]; then
  echo "                                            "
  echo "Please install enum4linux and rerun the script."
  echo "                                            "
  exit 0
fi

# go ahead and start scanning     
   
echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#          \e[36m   TCP Scan  \e[35m           #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"

nmap -Pn -p- -A $1 -r -n --open

echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#          \e[36m  Nikto Scan  \e[35m          #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"

nikto -h http://$1/

echo "                            "

nikto -h https://$1/

echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#          \e[36m   Dirb Scan  \e[35m          #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"

dirb http://$1/ /usr/share/wordlists/dirb/big.txt

echo "                            "

dirb https://$1/ /usr/share/wordlists/dirb/big.txt

echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#          \e[36m Enum4linux  \e[35m           #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"

enum4linux $1

echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#          \e[36m Happy Hunting!  \e[35m       #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"

