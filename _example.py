#! /usr/bin/env python3
"""
	Examble use of localPTZtime MicroPython module with ntp
	
	:author:	Roberto Bellingeri
	:copyright:	Copyright 2023 - NetGuru
	:license:	GPL
"""

import network
import time
import ntptime
import localPTZtime


WIFI_SSID = "NG" #"-your-wifi-ssid-"
WIFI_PASSWORD = "TheodoreRoosevelt" #"-your-wifi-password-"
WIFI_MAXWAIT = 10

# Definition string in Posix Time Zone notation
PTZ = "CET-1CEST,M3.5.0,M10.5.0/3"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

n = 0

while (n < WIFI_MAXWAIT):
	if ((wlan.status() < 0) or (wlan.status() >= 3)):
		break
	n += 1
	print("Waiting for connection...")
	time.sleep(1)

if (wlan.status() != 3):
	raise RuntimeError("Network connection failed")
else:
	print("Connected")
	print("ip:\t" + wlan.ifconfig()[0])

	t = time.time()
	t_tuple_gmt = time.gmtime(t)
	t_tuple_local = localPTZtime.tztime(t, PTZ)

	# Print GMT time tuple
	print(f"GMT time before synchronization:\t{t_tuple_gmt}")
	# Print Local time tuple
	print(f"Local time before synchronization:\t{t_tuple_local}")

	# NTP synchronization
	ntptime.settime()

	t = time.time()
	t_tuple_gmt = time.gmtime(t)
	t_tuple_local = localPTZtime.tztime(t, PTZ)

	# Print GMT time tuple
	print(f"GMT time after synchronization:\t\t{t_tuple_gmt}")
	# Print Local time tuple
	print(f"Local time after synchronization:\t{t_tuple_local}")
