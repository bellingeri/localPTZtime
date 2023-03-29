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

Result can be check here:
* https://www.epochconverter.com/

## File

All the module is in *localPTZtime.py*, *_test.py* is for testing purposes and *_example.py* is an example described later.

## Functions

The module provides these functions:

* **tztime(timestamp, ptz_string, zone_designator)**<br>
  Does all the work.

* **checkptz(ptz_string)**<br>
  Posix Time Zone string formal test.<br>
  In MicroPython it always returns 'None' because re.fullmatch() is not defined.

## Usage example on MicroPython

### Simple use

~~~python
# Import module
import localPTZtime

# Define the timestamp
timestamp = 1678689000

# Define the Posix Time Zone
ptz_string = "CET-1CEST,M3.5.0,M10.5.0/3"

# Call tztime() function:
isotime = localPTZtime.tztime(timestamp, ptz_string)

# Print result
print(isotime)
~~~

Expected result is:
> **'2023-03-13T07:30:00+01'**

The function tztime() can also be callable with a third parameter which, if set to False, disables the "zone designator" (`+1` in this example) as described here: https://en.wikipedia.org/wiki/ISO_8601#Time_zone_designators

### More advanced use

An example using NTP synchronization can be seen in the [_example.py](_example.py) file.
You will only need to set the Wi-Fi data and the definition string.

## To Do

1. Test for various timezones and special cases.
