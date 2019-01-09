echo "#------------------------------------------------#"
echo "#         SUID Files Enumeration Script          #"
echo "#------------------------------------------------#"
echo "                                                 "

#Find SUID files and store them in SUID_FILES.txt
echo "[+] Dumping SUID files list into SUID_FILES.txt.."
find / \( -perm -4000 \) -exec ls -ld {} \; 2>/dev/null | awk '{print $9}' > SUID_FILES.txt
sleep 2

#loop through common linux binaries and then remove them from SUID_FILES.txt
echo "[+] Trimming common SUID files from SUID_FILES.txt..."

for bname in '/umount/d' '/su/d' '/mount/d' '/sudo/d' '/passwd/d' '/exim4/d' '/chfn/d' '/chsh/d' '/procmail/d' '/newgrp/d' '/ping/d' '/ntfs-3g/d' '/pppd/d' '/pkexec/d' '/ssh-keysign/d' '/dbus-daemon-launch-helper/d' '/uuidd/d' '/pt_chown/d' '/at/d' '/mtr/d' '/dmcrypt-get-device/d' '/X/d' '/traceroute6.iputils/d' '/polkit-resolve-exe-helper/d' '/polkit-set-default-helper/d' '/polkit-grant-helper-pam/d'

do
  sed -i $bname ./SUID_FILES.txt
done
sleep 2

echo "[+] Preform strings on the following binaries.."
echo "                                                  "  
echo "#------------------------------------------------#"
for line in $(cat SUID_FILES.txt); do                              
echo " * "$line
done 
echo "#------------------------------------------------#"
echo "                                                  " 
sleep 5

# Perform string command on uncommon SUID binaries
for line in $(cat SUID_FILES.txt); do 
  echo "             "
  echo "#------------------------------------------------#"
  echo $line
  echo "#------------------------------------------------#"
  strings $line
  echo "                                                  "
  sleep 5
done
echo "                                                  " 
echo "#------------------------------------------------#"
echo "#           Done. Happy hunting!                 #"
echo "#------------------------------------------------#"


