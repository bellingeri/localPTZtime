#! /usr/bin/env python3
"""
	Some test for localPTZtime MicroPython module
	
	:author:	Roberto Bellingeri
	:copyright:	Copyright 2023 - NetGuru
	:license:	GPL
"""

import time
import localPTZtime
import sys
import os

# Check python implementation
if sys.implementation.name != "micropython":	# type: ignore
												# Set timezone to "Etc/GMT" for testing purposes; That way Python functions don't come to play with time zone and daylight saving time.
	os.environ['TZ'] = "Etc/GMT"				# type: ignore
	if hasattr(time, 'tzset'):
												# time.tzset() should be called on Linux, but doesn't exist on Windows. time.tzset() is not defined in MicroPython.
		time.tzset()							# type: ignore

color = {
	'red': "\033[91m",
	'green': "\033[92m",
	'none': "\033[0m"
	}

test = list()

test = [
	# PosixTimeZone string, timestamp to test, desiderable output
	["GMT0", 1679792399, "2023-03-26T00:59:59"],							#UTC 2023-03-26 00:59:59 - Std for GMT

	["CET-1CEST,M3.5.0,M10.5.0/3", 1679792399, "2023-03-26T01:59:59"],		#UTC 2023-03-26 00:59:59 - Before dst change for Europe/Rome
	["CET-1CEST,M3.5.0,M10.5.0/3", 1679792400, "2023-03-26T03:00:00"],		#UTC 2023-03-26 01:00:00 - After dst change for Europe/Rome
	["CET-1CEST,M3.5.0,M10.5.0/3", 1698541199, "2023-10-29T02:59:59"],		#UTC 2023-10-29 00:59:59 - Before std change for Europe/Rome
	["CET-1CEST,M3.5.0,M10.5.0/3", 1698541200, "2023-10-29T02:00:00"],		#UTC 2023-10-29 01:00:00 - After std change for Europe/Rome

	["CET-1CEST,M3.5.0,M10.5.0/3", 1743296399, "2025-03-30T01:59:59"],		#UTC 2025-03-30 00:59:59 - Before dst change
	["CET-1CEST,M3.5.0,M10.5.0/3", 1743296400, "2025-03-30T03:00:00"],		#UTC 2025-03-30 01:00:00 - After dst change

	["GMT0BST,M3.5.0/1,M10.5.0", 1679792399, "2023-03-26T00:59:59"],		#UTC 2023-03-26 00:59:59 - Before dst change for Europe/London
	["GMT0BST,M3.5.0/1,M10.5.0", 1679792400, "2023-03-26T02:00:00"],		#UTC 2023-03-26 01:00:00 - After dst change for Europe/London
	["GMT0BST,M3.5.0/1,M10.5.0", 1698541199, "2023-10-29T01:59:59"],		#UTC 2023-10-29 00:59:59 - Before std change for Europe/London
	["GMT0BST,M3.5.0/1,M10.5.0", 1698541200, "2023-10-29T01:00:00"],		#UTC 2023-10-29 01:00:00 - After std change for Europe/London

	["EST5EDT,M3.2.0,M11.1.0", 1678604399, "2023-03-12T01:59:59"],			#UTC 12-03-2023 06:59:59 - Before dst change for America/New_York
	["EST5EDT,M3.2.0,M11.1.0", 1678604400, "2023-03-12T03:00:00"],			#UTC 12-03-2023 07:00:00 - After dst change for America/New_York
	["EST5EDT,M3.2.0,M11.1.0", 1699163999, "2023-11-05T01:59:59"],			#UTC 2023-11-05 05:59:59 - Before std change for America/New_York
	["EST5EDT,M3.2.0,M11.1.0", 1699164000, "2023-11-05T01:00:00"],			#UTC 2023-11-05 06:00:00 - After std change for America/New_York

	["AEST-10AEDT,M10.1.0,M4.1.0/3", 1696089599, "2023-10-01T01:59:59"],	#UTC 2023-09-30 15:59:59 - Before dst change for Australia/Sydney
	["AEST-10AEDT,M10.1.0,M4.1.0/3", 1696089600, "2023-10-01T03:00:00"],	#UTC 2023-09-30 16:00:00 - After dst change for Australia/Sydney
	["AEST-10AEDT,M10.1.0,M4.1.0/3", 1680364799, "2023-04-02T02:59:59"],	#UTC 2023-04-01 15:59:59 - Before std change for Australia/Sydney
	["AEST-10AEDT,M10.1.0,M4.1.0/3", 1680364800, "2023-04-02T02:00:00"],	#UTC 2023-04-01 16:00:00 - After std change for Australia/Sydney

	["<+11>-11<+12>,M10.1.0,M4.1.0/3", 1696085999, "2023-10-01T01:59:59"],	#UTC 2023-09-30 14:59:59 - Before dst change for Pacific/Norfolk
	["<+11>-11<+12>,M10.1.0,M4.1.0/3", 1696086000, "2023-10-01T03:00:00"],	#UTC 2023-09-30 15:00:00 - After dst change for Pacific/Norfolk
	["<+11>-11<+12>,M10.1.0,M4.1.0/3", 1680361199, "2023-04-02T02:59:59"],	#UTC 2023-04-01 14:59:59 - Before std change for Pacific/Norfolk
	["<+11>-11<+12>,M10.1.0,M4.1.0/3", 1680361200, "2023-04-02T02:00:00"],	#UTC 2023-04-01 15:00:00 - After std change for Pacific/Norfolk

	["KST-9", 1672527600, "2023-01-01T08:00:00"],							#UTC 2022-12-31 23:00:00 - Std for Asia/Seoul over year change

	["<-04>4<-03>,M10.1.0/0,M3.4.0/0", 1696132799, "2023-09-30T23:59:59"],	#UTC 2023-10-01 07:59:59 - Before dst change for America/Asuncion
	["<-04>4<-03>,M10.1.0/0,M3.4.0/0", 1696132800, "2023-10-01T01:00:00"],	#UTC 2023-10-01 08:00:00 - After dst change for America/Asuncion
	["<-04>4<-03>,M10.1.0/0,M3.4.0/0", 1679799599, "2023-03-25T23:59:59"],	#UTC 2023-03-26 02:59:59 - Before std change for America/Asuncion
	["<-04>4<-03>,M10.1.0/0,M3.4.0/0", 1679799600, "2023-03-25T23:00:00"],	#UTC 2023-03-26 03:00:00 - After std change for America/Asuncion
	
]

n = n_ok = n_ko = 0

for ts in test:
	n += 1
	print("---------------------------")
	if (localPTZtime.checkptz(ts[0]) != False):
		print("PTZ:\t\t" + str(ts[0]))
		print("TS:\t\t" + str(ts[1]))
		print("Desired:\t" + str(ts[2]))

		ts_local=localPTZtime.tziso(ts[1], ts[0])
		print("Calculated:\t" + ts_local)

		if (ts_local[:19]==ts[2]):  # comparison between calculated (without zone designator) and desired.
			print(f"Result:\t\t{color['green']}OK{color['none']}")
			n_ok += 1
		else:
			print(f"Result:\t\t{color['red']}KO{color['none']}")
			n_ko += 1
	else:
		print(f"Error in PTZ string: {color['red']}{ts[0]}{color['none']}")
		n_ko += 1

print("\n\n--Test results--")
print(f"Number of checks:\t{n}")
print(f"Successful checks:\t{n_ok}")
print(f"Failed checks:\t\t{n_ko}")
