#!/usr/bin/python

import socket
import time
try:
	import hexdump
except:
	print '[+] Please install python "hexdump" module'
	print '[+] sudo easy_install hexdump'
	exit()

host = 'XX.XX.XX.XX'
port = 36000
logfile = 'chuilang2014_emulate.log'
f = open(logfile,'a')

check_in = (
	'\x01\x00\x00\x00\x6b\x00\x00\x00\x00\xf4\x01\x00\x00\x32\x00\x00'+
	'\x00\xe8\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'+
	'\x00\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\xac\x10\xa1\x82'+
	'\xac\x10\xa1\x82\xac\x10\xa1\x82\xac\x10\xa1\x82\xac\x10\xa1\x82'+
	'\xff\xff\x01\x00\x00\x00\x00\x00\x63\x68\x75\x6c\x69\x61\x6e\x67'+
	'\x32\x30\x31\x34\x3a\x00\x01\x00\x00\x00\xaf\x0b\x00\x00\xff\x03'+
	'\x00\x00\x57\x69\x6e\x64\x6f\x77\x73\x20\x58\x50\x00\x47\x32\x2e'+
	'\x32\x35\x00')

heartbeat = (
'\x02\x00\x00\x00\x21\x00\x00\x00'+
'\x01\x65\x3b\x00\x00\x00\x00\x00'+
'\x00\x00\x00\x00\x00\x00\x10\x00'+
'\x00\x00\x00\x02\x01\x64\x00\x00'+
'\x00\x00\x00\x00\x00\x00\x00\x00')

def communicate():
	while 1:
		#print '[+] sending payload...'
		response = s.recv(8)
		print '[+] Response received'
		print '[+] '+response.encode("hex")
		print '[+] Sending response...'
		s.send(check_in)
		print '[+] Waiting for response...'
		heartbeat_response = s.recv(1024)
		print '[+] \t\t\tResponse '
		print '\033[93m'+'='*76+'\033[0m'
		print hexdump.hexdump(heartbeat_response)
		print '\033[93m'+'='*76+'\033[0m'
		f.write(heartbeat_response.encode('hex'))

		#time.sleep(10)

def checkin():
	s.send(check_in)
	initial_response = s.recv(1024)
	f.write(initial_response.encode('hex'))
	print '[+] \t\t\tInitial Response '
	print '\033[93m'+'='*76+'\033[0m'
	print hexdump.hexdump(initial_response)
	print '\033[93m'+'='*76+'\033[0m'
	print '[+] Sending initial heartbeat...'
	s.send(heartbeat)
	communicate()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print '[+] Connecting to host...'
s.connect((host, port))

try:
	checkin()
except KeyboardInterrupt:
	print '[+] Exiting...'
	f.close()
	s.close()
	exit()


