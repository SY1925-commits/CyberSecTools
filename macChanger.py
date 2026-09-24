import subprocess
import optparse
import re

def getArgs():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--newMACaddress", dest="newMAC", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help or -h for more information")
    elif not options.newMAC:
        parser.error("[-] Please specify a MAC address, use --help or -h for more information")
    return options

def changeMAC(interface, newMAC):
    print("> Changing MAC address for " + interface + " interface to " + newMAC)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMAC])
    subprocess.call(["ifconfig", interface, "up"])

def readNowMAC(interface):
    ifconfig_res = subprocess.check_output(
        ["ifconfig", interface]).decode()  # decode() for python 3 compatibility
    nowMAC = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_res)
    if nowMAC:
        return nowMAC.group(0)
    else:
        print("[-] Could not read MAC address")

def verifyNewMAC(interface, MACvalue):
    currentMAC = readNowMAC(interface)
    if currentMAC == MACvalue:
        print("[+] MAC address successfully changed to " + currentMAC)
    else:
        print("[-] Could not change MAC address")

options = getArgs()

currentMAC = readNowMAC(options.interface)
print("Current MAC = " + str(currentMAC))

changeMAC(options.interface, options.newMAC)

verifyNewMAC(options.interface, options.newMAC)