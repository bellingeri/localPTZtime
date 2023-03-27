#! /usr/bin/env python3

import localPTZtime
import time

test = list()

test = [
	# PosixTimeZone string, timestamp to test, desiderable output
	["GMT0", 1679792399, "2023-03-26T00:59:59"],

	["CET-1CEST,M3.5.0,M10.5.0/3", 1679792399, "2023-03-26T01:59:59"],		#UTC 26-03-2023 00:59:59 - Before dst for Europe/Rome
	["CET-1CEST,M3.5.0,M10.5.0/3", 1679792400, "2023-03-26T03:00:00"],		#UTC 26-03-2023 01:00:00 - After dst for Europe/Rome
	["CET-1CEST,M3.5.0,M10.5.0/3", 1698541199, "2023-10-29T02:59:59"],		#UTC 29-10-2023 00:59:59 - Before std for Europe/Rome
	["CET-1CEST,M3.5.0,M10.5.0/3", 1698541200, "2023-10-29T02:00:00"],		#UTC 29-10-2023 01:00:00 - After std for Europe/Rome

	["GMT0BST,M3.5.0/1,M10.5.0", 1679792399, "2023-03-26T00:59:59"],		#UTC 26-03-2023 00:59:59 - Before dst for Europe/London
	["GMT0BST,M3.5.0/1,M10.5.0", 1679792400, "2023-03-26T02:00:00"],		#UTC 26-03-2023 01:00:00 - After dst for Europe/London
	["GMT0BST,M3.5.0/1,M10.5.0", 1698541199, "2023-10-29T01:59:59"],		#UTC 29-10-2023 00:59:59 - Before std for Europe/London
	["GMT0BST,M3.5.0/1,M10.5.0", 1698541200, "2023-10-29T01:00:00"],		#UTC 29-10-2023 01:00:00 - After std for Europe/London

	["EST5EDT,M3.2.0,M11.1.0", 1678604399, "2023-03-12T01:59:59"],			#UTC 12-03-2023 06:59:59 - Before dst for America/New_York
	["EST5EDT,M3.2.0,M11.1.0", 1678604400, "2023-03-12T03:00:00"],			#UTC 12-03-2023 07:00:00 - After dst for America/New_York
	["EST5EDT,M3.2.0,M11.1.0", 1699163999, "2023-11-05T01:59:59"],			#UTC 05-11-2023 05:59:59 - Before std for America/New_York
	["EST5EDT,M3.2.0,M11.1.0", 1699164000, "2023-11-05T01:00:00"],			#UTC 05-11-2023 06:00:00 - After std for America/New_York

	["AEST-10AEDT,M10.1.0,M4.1.0/3", 1696089599, "2023-10-01T01:59:59"],	#UTC 30-09-2023 15:59:59 - Before dst for Australia/Sydney
	["AEST-10AEDT,M10.1.0,M4.1.0/3", 1696089600, "2023-10-01T03:00:00"],	#UTC 30-09-2023 16:00:00 - After dst for Australia/Sydney
	["AEST-10AEDT,M10.1.0,M4.1.0/3", 1680364799, "2023-04-02T02:59:59"],	#UTC 01-04-2023 15:59:59 - Before std for Australia/Sydney
	["AEST-10AEDT,M10.1.0,M4.1.0/3", 1680364800, "2023-04-02T02:00:00"],	#UTC 01-04-2023 16:00:00 - After std for Australia/Sydney
	
]

for ts in test:
	if (localPTZtime.checkptz(ts[0]) != False):
		print("---------------------------")
		print("PTZ:\t\t" + str(ts[0]))
		print("TS:\t\t" + str(ts[1]))
		print("UTC:\t\t" + time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(ts[1])))
		print("Local:\t\t" + str(ts[2]))

		ts_local=localPTZtime.tztime(ts[1], ts[0])
		print("TS local:\t" + ts_local)
		if (ts_local[:19]==ts[2]):
			print("Result:\t\t\033[92mOK\033[0m")
		else:
			print("Result:\t\t\033[91mKO\033[0m")
