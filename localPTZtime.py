#! /usr/bin/env python3
"""
	Method to convert time - in seconds passed since Unix epoch - from GMT time zone to given time zone expressed in Posix Time Zone format.
	
	:author:	Roberto Bellingeri
	:copyright:	Copyright 2023 - NetGuru
	:license:	GPL
"""

"""
	Changelog:
	
	0.0.1	
			initial release
"""

__version__ = "0.0.1"


import time
import re

def checkptz(ptz_string: str):
	"""
	Check if the format of the string complies with what is described here: https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html
	Only for testing purposes: on MicroPython always return 'None'.

	Parameters:
	ptz_string (str): String in Posix Time Zone format
	
	Returns:
	bool: Test result
	"""
	ptz_string = _normalize(ptz_string)
	
	result = None

	if hasattr(re, 'fullmatch'):							# re.fullmatch() is not defined in MicroPython
		check_re = r"^"
		check_re += r"([^:\d+-]){3,}"  # std
		check_re += r"[+-]?\d{1,2}(:\d{1,2}){0,2}" # std offset
		
		check_re += r"(([^:\d+-,]){3,}"  # dst, can be omitted
		check_re += r"(([+-]?\d{1,2}(:\d{1,2}){0,2})?" # dst offset, can be omitted
		
		check_re += r","  #dst start
		check_re += r"("
		check_re += r"(J\d{1,3})"  #day, leap years don't count 
		check_re += r"|"
		check_re += r"(\d{1,3})"  #day, leap years count 
		check_re += r"|"
		check_re += r"(M([1-9]|1[0-2]).[1-5].[0-6])"  # month.week.day
		check_re += r")"

		check_re += r"(\/\d{1,2}(:\d{1,2}){0,2})?"  # time, can be omitted

		check_re += r","  #dst end
		check_re += r"("
		check_re += r"(J\d{1,3})"  #day, leap years don't count
		check_re += r"|"
		check_re += r"(\d{1,3})"  #day, leap years count
		check_re += r"|"
		check_re += r"(M([1-9]|1[0-2]).[1-5].[0-6])"  # month.week.day
		check_re += r")"

		check_re += r"(\/\d{1,2}(:\d{1,2}){0,2})?"  # time, can be omitted
		
		check_re += r")" # dst offset end

		check_re += r")?" # dst end
		
		check_re += r"$"

		#print(check_re)

		if (re.fullmatch(check_re,ptz_string) == None):		# type: ignore
			result = False
		else:
			result = True

	return result


def tztime(timestamp: float, ptz_string: str, zone_designator = True):
	"""
	Return an ISO 8601 date and time string according to the time zone provided in Posix Time Zone format

	Parameters:
	timestamp (float): Time in second
	ptz_string (str): Time zone in Posix format
	zone_designator (bool): Insert zone designator in returned string - default: True
	
	Returns:
	string: ISO 8601 date and time string
	"""
	ptz_string = _normalize(ptz_string)

	std_offset_seconds = 0
	dst_offset_seconds = 0
	tot_offset_seconds = 0

	ptz_parts = ptz_string.split(",")

	#offsetHours = re.split(r"[^\d\+\-\:]+", ptz_parts[0])
	offsetHours = re.compile(r"[^\d\+\-\:]+").split(ptz_parts[0])  # re.compile() is used for MicroPython compatibility
	offsetHours = list(filter(None, offsetHours))
	#print(offsetHours)

	if (len(offsetHours) > 0):

		std_offset_seconds = - _hours2secs(offsetHours[0])

		if (len(offsetHours)>1):
			dst_offset_seconds = _hours2secs(offsetHours[1])
		else:
			dst_offset_seconds = 3600

	#print("timestamp:\t" + str(int(timestamp)))

	if (len(ptz_parts)==3):
		year = time.gmtime(int(timestamp))[0]
		dst_start = _parseposixtransition(ptz_parts[1], year)
		dst_end = _parseposixtransition(ptz_parts[2], year)

		if (dst_start < dst_end):							#northern hemisphere
			if ((timestamp + std_offset_seconds) < dst_start):
				tot_offset_seconds = std_offset_seconds
			elif ((timestamp + std_offset_seconds + dst_offset_seconds) < dst_end):
				tot_offset_seconds =  std_offset_seconds + dst_offset_seconds
			else:
				tot_offset_seconds =  std_offset_seconds
		else:												# southern hemisphere
			if ((timestamp + std_offset_seconds + dst_offset_seconds) < dst_end):
				tot_offset_seconds = std_offset_seconds + dst_offset_seconds
			elif ((timestamp + std_offset_seconds) < dst_start):
				tot_offset_seconds = std_offset_seconds
			else:
				tot_offset_seconds = std_offset_seconds + dst_offset_seconds
		
		#print("dstOffset:\t" + str(dst_offset_seconds))
		#print("dstStart:\t" + str(dst_start) + "\t" + str(time.gmtime(dst_start)))
		#print("dstEnd:  \t" + str(dst_end) + "\t" + str(time.gmtime(dst_end)))

	else:
		tot_offset_seconds = std_offset_seconds

	timemod = timestamp + tot_offset_seconds

	tx = time.gmtime(int(timemod))
	stx = f"{tx[0]}-{tx[1]:02d}-{tx[2]:02d}T{tx[3]:02d}:{tx[4]:02d}:{tx[5]:02d}"
	if (zone_designator == True):
		stx += _secs2zonedesignator(tot_offset_seconds)

	return stx


def _normalize(ptz_string: str):
	"""
	Return simple normalization of PTZ string

	Parameters:
	ptz_string (str): PTZ string

	Returns:
	str: Normalized PTZ string

	"""
	ptz_string = ptz_string.upper()
	ptz_string = re.compile(r"\<[^\>]*\>").sub("DUMMY",ptz_string) # For what appear to be non-standard strings like "<+11>-11<+12>,M10.1.0,M4.1.0/3"

	return ptz_string


def _parseposixtransition(transition: str, year: int):
	"""
	Returns the moment of the transition from std to dst and vice-versa

	Parameters:
	transition (str): Part of Posix Time Zone string related to the transition
	year (int): The year
	
	Returns:
	float: Time adjusted
	"""
	parts = transition.split('/')
	seconds = 0
	tr = 0

	if (len(parts) == 2):
		seconds = _hours2secs(parts[1])

	else:
		seconds = 2 * 3600
	
	
	if (transition[0] == "M"):
		date_parts = parts[0][1:].split('.')
		if (len(date_parts)==3):
			month = int(date_parts[0])  # month from '1' to '12'
			week_of_month = int(date_parts[1])  # week number from '1' to '5'. '5' always the last.
			day_of_week = int(date_parts[2])  # day of week - 0:Sunday 1:Monday 2:Tuesday 3:Wednesday 4:Thursday 5:Friday 6:Saturday

			base_year = 1970
			base_year_1st_day = 4 # the first day of the year 1970 was Thursday

			month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
			if ((((year % 4) == 0) and ((year % 100) != 0)) or (year % 400) == 0):
				month_days[1] = 29

			# calculate the number of days since 1/1/base_year
			days_since_base_date = (year - base_year) * 365 + (year - base_year - 1) // 4
			days_since_base_date += sum(month_days[:month - 1])

			# calculate the day of the week for the first day of month
			first_day_of_month = (days_since_base_date + base_year_1st_day) % 7

			# calculate the day of the month
			day_of_month = 1 + (week_of_month - 1) * 7 + (day_of_week - first_day_of_month) % 7

			if day_of_month > month_days[month - 1]:
				day_of_month -= 7
			
			tr = time.mktime((year, month, day_of_month, 0, 0, 0, 0, 0, 0))
		
	elif (transition[0] == "J"):
		day_num = int(parts[0][1:])
		if ((((year % 4) == 0) and ((year % 100) != 0)) or (year % 400) == 0):
			day_num += 1
		tr = time.mktime((year,1,1,0,0,0,0,0,0)) + (day_num * 86400)

	else:
		day_num = int(parts[0][1:])
		tr = time.mktime((year,1,1,0,0,0,0,0,0)) + ((day_num + 1) * 86400)

	return tr + seconds


def _hours2secs(hours: str):
	"""
	Convert hours string in seconds

	Parameters:
	hours (str): Hours in format 00[:00][:00]
	
	Returns:
	int: seconds
	"""
	seconds = 0

	hours_parts = hours.split(':')

	if (len(hours_parts)>0):
		seconds = int(hours_parts[0]) * 3600
		if (len(hours_parts)>1):
			seconds += int(hours_parts[1]) * 60
			if (len(hours_parts)>2):
				seconds += int(hours_parts[2])
	
	return seconds


def _secs2zonedesignator(sec: int):
	"""
	Convert seconds in hours:mins string for ISO 8601

	Parameters:
	sec (int): seconds
	
	Returns:
	str: Hours in format 00:00
	"""
	output = ""

	if (sec != 0):
		output = f"{(sec // 3600):+03d}"
		
		mins = abs(sec) % 3600
		if (mins != 0):
			output += ":" + f"{(mins // 60):02d}"
	else:
		output = "Z"
	
	return output