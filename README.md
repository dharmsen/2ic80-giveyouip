# 2ic80-giveyouip

This arp poisoning/dns spoofing tool was made for educational purposes only.
This tool was developed for the final project of the course 2IC80 Lab on Offensive Computer Security at the Eindhoven University of Technology.

---

The repository is split up in two folders:
- Combined
- Seperate

For Combined, the main file `giveyouip.py` runs the attack for you. Arguments/flags that can be passed are:
- `-t`, `--target`: target IP to attack **(required)**
- `-g`, `--gateway`: gateway IP of the local network **(required)**
- `-m`, `--me`: IP of the server the DNS spoof is routed to instead **(required)**
- `-i`, `--interface`: interface to operate the attack on **(required)**
- `-s`, `--sslstrip`: enable ssl stripping
- `-d`, `--dns`: enable dns spoofing
- `-o`, `--dns-overkill`: enable dns spoofing for all dns messages (spoof every domain) 

This script is not yet functional.

For Seperate, the files are ran seperately, in the following order:
1. `ssl.py` (not required)
2. `arp.py`
3. `dns.py`/`dns_overkill.py`

Arguments are provided in the files.
