#!/usr/bin/env python

#How to run:
	#0. run		python scanner.py -t 10.0.2.1/24
             


import scapy.all as scapy
import argparse

def scan(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]

    clients_list = []

    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(result_print):
    print("IP\t\t\tMAC Address\n--------------------------------------------------")
    for client in result_print:
        print(client["ip"] + "\t\t" + client["mac"])

# def get_arguments():
#     nando = optparse.OptionParser()
#     nando.add_option("-t", "--target", dest = "target", help = "Input your target input")
#     (options,arguments) = nando.parse_args()
#     return options

def get_arguments():
    nando = argparse.ArgumentParser()
    nando.add_argument("-t", "--target", dest = "target", help = "Input your IP target")
    option = nando.parse_args()
    return option

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
