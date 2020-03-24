# final-program
All final program for play


echo 1 > /proc/sys/net/ipv4/ip_forward


How to install Scapy :  https://www.youtube.com/watch?v=3tkVKflR4rY


How to install netfilterqueue:
    apt-get update
    apt-get install build-essential python-dev libnetfilter-queue-dev
    pip install NetfilterQueue


   iptables -I FORWARD -j NFQUEUE --queue-num 0 
   iptables --flush
    
