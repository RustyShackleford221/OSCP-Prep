import socket
import os

# host to listen on
host = "localhost"

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

# read a single packet
print(sniffer.recvfrom(65565))

# if we're on Windows, turn promuscous mode off
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)