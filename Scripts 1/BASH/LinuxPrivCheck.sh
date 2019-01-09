
#---------------------------------------------------------------------------------#
# Name       = Linux Quick n' Dirty Privilege Escalation Check Script             #
# Reference  = https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/ #
# Author     = @ihack4falafel                                                     #
# Date       = 12/17/2017                                                          #
# Usage      = chmod +x LinuxPrivCheck.sh && ./LinuxPrivCheck.sh                  #
#---------------------------------------------------------------------------------#

echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#          \e[36m OS Information  \e[35m       #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"
uname -a                                                                                                # Kernel Version
cat /etc/issue                                                                                          # Distribution
cat /etc/*release                                                                                       # OS Release
echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#        \e[36m Network Information  \e[35m    #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"
cat /etc/resolv.conf                                                                                    # Nameservers
cat /etc/hosts                                                                                          # Hosts
route -n                                                                                                # Route Info.
iptables -L                                                                                             # Firewall Rules
cat /etc/network/interfaces                                                                             # Network Interfaces 
echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#       \e[36m Password Information     \e[35m #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"
echo -e "\e[34m"
echo "----------|Password File|-----------"
echo "                                    "
echo -e "\e[39m"
cat /etc/passwd  
echo "                                    "                                                              # Password File
echo -e "\e[39m"
echo -e "\e[34m"
echo "-----------|Shadow File|------------"
echo "                                    "
echo -e "\e[39m"
cat /etc/shadow                                                                                          # Shadow File
echo "                                    "
echo -e "\e[34m"
echo "                                    "
echo "------------|SSH Keys|--------------"
echo "                                    "
echo -e "\e[39m"
cat /root/.ssh/authorized_keys                                                                           # Authorized SSH Keys
cat /root/.ssh/known_hosts                                                                               # SSH Known Hosts
cat ~/.ssh/id_rsa                                                                                        # RSA Keys
cat ~/.ssh/id_dsa                                                                                        # DSA Keys
cat /etc/ssh/ssh_host_dsa_key                                                                            # Alernative DSA keys
cat /etc/ssh/ssh_host_rsa_key                                                                            # Alternative RSA Keys
echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#         \e[36m Misc. Information  \e[35m     #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"
echo -e "\e[34m"
echo "------|Important Executables|-------"
echo -e "\e[39m"
echo "                                    "
which wget                                                                                               # Check Wget
which nc                                                                                                 # Check Nc
which netcat                                                                                             # Check Netcat
which python                                                                                             # Check Python
which python3                                                                                            # Check Python3
which gcc                                                                                                # Check GCC
which perl                                                                                               # Check Perl
echo -e "\e[34m"
echo "                                    "
echo "-----------|Sudoers File|-----------"
echo "                                    "
echo -e "\e[39m"
cat /etc/sudoers                                                                                         # Check Sudoers
echo -e "\e[34m"
echo "                                    "
echo "--------------|Users|---------------"
echo "                                    "
echo -e "\e[39m"
cat /etc/passwd | cut -d: -f1                                                                            # List Users
echo -e "\e[34m"
echo "                                    "
echo "-------------|Groups|---------------"
echo "                                    "
echo -e "\e[39m"
cat /etc/group                                                                                           # Check Groups
echo -e "\e[34m"
echo "                                    "
echo "-----------|SUID Files|-------------"
echo "                                    "
echo -e "\e[39m"
find / -type f -perm -u=s -exec ls -la {} + 2>/dev/null                                                  # Check SUID Files 
echo -e "\e[34m"
echo "                                    "
echo "-----------|GUID Files|-------------"
echo "                                    "
echo -e "\e[39m"
find / -type f -perm -g=s -exec ls -la {} + 2>/dev/null                                                  # Check GUID Files 
echo -e "\e[34m"
echo "                                    "
echo "-----------|NO ROOT SQUASH|---------"
echo "                                    "
echo -e "\e[39m"                                                                                         # check no_root_squash
if [ $(cat /etc/exports 2>/dev/null | grep no_root_squash | wc -c) -ne 0 ]
then
  echo "NO_ROOT_SQUASH FOUND! " && cat /etc/exports | grep no_root_squash
else
  echo "NO_ROOT_SQUASH NOT FOUND!"
fi
echo -e "\e[34m"
echo "                                    "
echo "----------------|EXIM|--------------"
echo "                                    "
echo -e "\e[39m"                                                                                         # Check exim              
if [ $(which exim | wc -c) -ne 0 ]
then
  echo -n "EXIM FOUND! " && exim -bV | grep version
else
  echo "EXIM NOT FOUND!"
fi
echo -e "\e[34m"
echo "                                    "
echo "-------------|CHKROOTKIT|-----------"
echo "                                    "
echo -e "\e[39m"                                                                                         # Check chkrootkit              
if [ $(which chkrootkit | wc -c) -ne 0 ]
then
  echo -n "CHKROOTKIT FOUND! " && chkrootkit -V
else
  echo "CHKROOTKIT NOT FOUND!"
fi
echo -e "\e[34m"
echo "                                    "
echo "-------------|MySQL Creds|-----------"
echo "                                    "
echo -e "\e[39m"                                                                                         # Check MySQL Creds              
if [ $(find / -iname wp-config.php 2>/dev/null | wc -c) -ne 0 ]
then
  echo "WP-CONFIG.PHP FOUND! " && cat $(locate wp-config.php) | grep DB_NAME && cat $(locate wp-config.php) | grep DB_USER && cat $(locate wp-config.php) | grep DB_PASSWORD 
else
  echo "WP-CONFIG.PHP NOT FOUND!"
fi
echo -e "\e[34m"
echo "                                    "
echo "--------------|FSTab|---------------"
echo "                                    "
echo -e "\e[39m"
cat /etc/fstab                                                                                           # Check Fstab
echo -e "\e[34m"
echo "                                    "
echo "---------|Daily Cron Jobs|----------"
echo "                                    "
echo -e "\e[39m"
ls -la /etc/cron.d/                                                                                       # Check Cron Jobs
ls -la /etc/cron.daily/                                                                                   # Alternative Check Cron Jobs
echo -e "\e[34m"
echo "                                    "
echo "-------------|Crontab|--------------"
echo "                                    "
echo -e "\e[39m"
cat /etc/crontab                                                                                         # Check Crontab
echo -e "\e[34m"
echo "                                    "
echo "------|World Writable Folders|------"
echo "                                    "
echo -e "\e[39m"
find / -perm -222 -type d 2>/dev/null                                                                     # World Wireable Folders
echo -e "\e[34m"
echo "                                    "
echo "-----------|Home Directory|---------"
echo "                                    "
echo -e "\e[39m"
ls -ahl /home/ 2>/dev/null                                                                                # Check Home Directory
echo "                                    "
touch ~/.bash_history                                                                                     # Clear Command History
echo    "                                          "
echo -e "\e[35m#----------------------------------#"
echo -e "\e[35m#   \e[36m Script has been completed!  \e[35m  #"
echo -e "\e[35m#----------------------------------#"
echo    "                                          "
echo -e "\e[39m"

