#!/usr/bin/env python

#How to run:
	#0. run		python mac_changer.py -i eth0 -m 00:11:22:33:44:55

import subprocess
import optparse
import re

def get_arguments():
    nando = optparse.OptionParser()
    nando.add_option("-i", "--interface", dest="interface", help="Choose interface")
    nando.add_option("-m", "--mac_adress", dest="mac_change", help="Choose your mac adress")
    (options,argumuments) = nando.parse_args()
    if not options.interface:
        nando.error("Input your interface properly")
    if not options.mac_change:
        nando.error("Coludn't find Mac Adress")
    return options

def mac_change(interface,mac_change):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_change])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_result:
        return mac_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

mac_change(options.interface, options.mac_change)

current_mac = get_current_mac(options.interface)
if current_mac == options.mac_change:
    print("[+] Mac address was succesfully changed to " + current_mac)
else:
    print("[-] Mac address didn't get change")

