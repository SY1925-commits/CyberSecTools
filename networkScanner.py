import scapy.all as scapy
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP Address")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify the target IP Address, use --help or -h for more information")
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip + "/24")
    brdcst = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_brdcst = brdcst/arp_request
    answeredList = scapy.srp(arp_brdcst, timeout=1, verbose=0)[0]

    clientsList = []
    for element in answeredList:
        clientInfo = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        clientsList.append(clientInfo)
    return clientsList

def printResult(resultsList):
    print("     IP\t\t\t\tMAC\n------------------------------------------")
    for client in resultsList:
        print(client["ip"] + "\t\t" + client["mac"])

scanResult = scan(getArgs().target)
printResult(scanResult)