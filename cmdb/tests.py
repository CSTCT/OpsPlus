from netaddr import *
ip = IPAddress('192.168.1.1')
if ip.is_private():
	print('yes')
else:
	print('no')