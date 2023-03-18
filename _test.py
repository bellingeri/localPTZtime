#! /usr/bin/env python3

import localPTZtime
import time

ptz = "CET-1CEST,M3.5.0,M10.5.0/3"							# Europe/Rome
#ptz = "CET-1CEST01:00:00,M3.5.0/02:00:00,M10.5.0/03:00:00"	# Europe/Rome (extended)

print("PTZ:\t" + ptz)

timestamp = list()

timestamp = [
	time.time(),	# Now
	
	1679792399,			#UTC 26-03-2023 00:59:59 - Before dst for Europe/Rome
	1679792400,			#UTC 26-03-2023 00:59:59 - After dst for Europe/Rome

	1698541199,			#UTC 29-10-2023 00:59:59 - Before std for Europe/Rome
	1698541200,			#UTC 29-10-2023 01:00:00 - After std for Europe/Rome
]

if localPTZtime.checkptz(ptz):

	for ts in timestamp:
		print("--------------------------- " + str(ts))
		#print("timestamp:\t" + str(ts))

		print("UTC:\t\t" + time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(ts)))
		print("Py local:\t" + time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(ts)))
		print("TZ local:\t" + time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(localPTZtime.tztime(ts, ptz))))
