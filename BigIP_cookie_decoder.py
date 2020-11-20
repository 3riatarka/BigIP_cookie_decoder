#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# HTTP Passive cookie implementation: https://web.archive.org/web/20150603012044/https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/ltm_configuration_guide_10_0_0/ltm_persist_profiles.html
# https://support.f5.com/csp/article/K83419154


### The cookie is implemented following these instructions:
# For example, the following string is a generated cookie template with the encoding automatically added, where [pool name] 
# is the name of the pool that contains the server, 336260299 is the encoded server address, and 20480 is the encoded port:
#
# Set-Cookie:BIGipServer[poolname]=336268299.20480.0000; expires=Sat, 01-Jan-2002 00:00:00 GMT; path=/
#
# To create your cookie from this template, type the actual pool name and an expiration date and time.
# Alternatively, you can perform the encoding using the following equation for address (a.b.c.d):
#
# d*(256^3) + c*(256^2) + b*256 +a
#
# The way to encode the port is to take the two bytes that store the port and reverse them. Thus, port 80 becomes 80 * 256 + 0 = 20480. 
# Port 1433 (instead of 5 * 256 + 153) becomes 153 * 256 + 5 = 39173. 
###

import sys, math

if len(sys.argv) != 2:
	print(f"Usage: {sys.argv[0]} <BigIP cookie value>")
	exit(1)

try:
	enc_ip, enc_port, trash = sys.argv[1].split('.')
	enc_ip = int(enc_ip)
	enc_port = int(enc_port)
except Exception as ex:
	print(f"[**] Error: unable to parse the cookie. Make sure the format is correct (three blocks separated by dots) -> {ex}")
	exit(1)

ip = ""
i = 0
while i <= 3:
	ip += str(int((enc_ip/256**i)%256))+"."
	i += 1
ip = ip[:-1]

port = int((enc_port%256)*256+(enc_port/256)%256)

print(f"IP: {ip}")
print(f"Port: {port}")