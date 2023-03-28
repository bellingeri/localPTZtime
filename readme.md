# localPTZtime

This MicroPython module allows the conversion of a timestamp with UTC timezone into other timezones expressed with the Posix Time Zone notation.
Returns a date in ISO 8601 format.

No dependencies on 'date', 'calendar', etc. modules; only 'time' and 're'.

A description of the Posix Time Zone format can be found at these addresses:
* https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html
* https://www.postgresql.org/docs/current/datetime-posix-timezone-specs.html

A complete list of strings - and the code to generate them starting from the database maintained by IANA (https://www.iana.org/time-zones), present on linux systems - can be find at this address:
* https://github.com/nayarsystems/posix_tz_db

ISO 8601 format can be find here:
* https://en.wikipedia.org/wiki/ISO_8601

## File

All the module is in *localPTZtime.py*, *_test.py* is for testing purposes.

## Functions

The module provides these functions:

* **tztime(timestamp, ptz_string, zone_designator)**
Does all the work.

* **checkptz(ptz_string)**
Posix Time Zone string formal test.
In MicroPython it always returns 'None' because re.fullmatch() is not defined.

## Usage example on MicroPython

Import module:
~~~python
import localPTZtime
~~~

Define the timestamp:
~~~python
timestamp = 1678689000
~~~

Define the Posix Time Zone:
~~~python
ptz_string = "CET-1CEST,M3.5.0,M10.5.0/3"
~~~

Call tztime() function:
~~~python
localPTZtime.tztime(timestamp, ptz_string)
~~~

Expected result is:
> **'2023-03-13T07:30:00+01'**

The function tztime() can also be called with a third parameter which, if set to False, disables the "zone designator" as described here: https://en.wikipedia.org/wiki/ISO_8601#Time_zone_designators


## To Do

1. Test for various timezones and special cases.
