import socket, os, struct, sys
#from netaddr import IPNetwork, IPAddress
from ctypes import *

# host to listen on
host = sys.argv[1]

# subnet to target

# IP header
class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # map protocol constants to ther ascii names
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        # human readable IP addresses
        # NOTES: "<" - little eindian | "L" - unsigned long
        #   struct.pack() return a bytes object
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

class ICMP(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass

# create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP # sniff all incoming IP packets, regardless of the protocol
else:
    socket_protocol = socket.IPPROTO_ICMP # sniff only ICMP packets

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 0))
# include the IP header in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# if we're listening on Windows, set the nic to promiscous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        # readpaket bytes
        raw_buffer = sniffer.recvfrom(65565)[0] # returns (bytes, address)
         # create an IP header from the first 20 bytes if the buffer
        ip_header = IP(raw_buffer[0:20]) # since raw_buffer is a bytes object (an immutable sequence 
                                         # in range [0, 255]), the "jumps" are made byte-by-byte
        # print the detected protocol and the hosts
        print("Protocol: {0} {1} -> {2}".format(ip_header.protocol, ip_header.src_address, ip_header.dst_address))

        # if it's ICMP, we want it
        if ip_header.protocol == "ICMP":
            # compute where our ICMP packet starts
            offset = ip_header.ihl * 4
            buff = raw_buffer[offset:offset + sizeof(ICMP)]

            # create a new ICMP structure
            icmp_header = ICMP(buff)

            print("ICMP -> Type: {0} Code: {1}".format(icmp_header.type, icmp_header.code))

# handle CTRL-C
except KeyboardInterrupt:
    # if we're on Windows, turn promuscous mode off
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)