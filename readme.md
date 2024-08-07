# localPTZtime

This MicroPython module allows the conversion of a timestamp with UTC timezone into other timezones expressed with the Posix Time Zone notation.
Can return a tuple in time_struct format or a string in ISO 8601 format.

No dependencies on 'date', 'calendar', etc. modules; only 'time' and 're'.

A description of the Posix Time Zone format can be found at these addresses:
* https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html
* https://www.postgresql.org/docs/current/datetime-posix-timezone-specs.html

A complete list of strings - and the code to generate them starting from the database maintained by IANA (https://www.iana.org/time-zones), present on linux systems - can be found at this address:
* https://github.com/nayarsystems/posix_tz_db

ISO 8601 format can be found here:
* https://en.wikipedia.org/wiki/ISO_8601

Result can be check here:
* https://www.epochconverter.com/

It's a work in progress: in particular, the parameters and return values have changed in the past and may change in the future.
When this happens, a GitHub release is made.

## Files

* *localPTZtime.py*: all functions are here.
* *_test.py*: is for testing purposes (MicroPython and CPython).
* *_example.py*: is an example described later.

## Functions

The module provides these functions:

#### tztime

```python
def tztime(timestamp: float, ptz_string: str)
```

Converts a time expressed in seconds in struct_time style 9-tuple according to the time zone provided in Posix Time Zone format

**Arguments**:

- `timestamp` _float_ - Time in second
- `ptz_string` _str_ - Time zone in Posix format
  

**Returns**:

  struct_time style tuple:
  * ``year``
  * ``month``
  * ``mday``
  * ``hour``
  * ``minute``
  * ``second``
  * ``weekday``
  * ``yearday``
  * ``isdst``


#### tziso

```python
def tziso(timestamp: float, ptz_string: str, zone_designator=True)
```

Return an ISO 8601 date and time string according to the time zone provided in Posix Time Zone format

**Arguments**:

- `timestamp` _float_ - Time in second
- `ptz_string` _str_ - Time Zone in Posix format
- `zone_designator` _bool_ - Insert zone designator in returned string - default: True
  

**Returns**:

- `string` - ISO 8601 date and time string


#### checkptz

```python
def checkptz(ptz_string: str)
```

Check if the format of the string complies with what is described here: https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html
Only for testing purposes: on MicroPython always return 'None'.

**Arguments**:

- `ptz_string` _str_ - String in Posix Time Zone format
  

**Returns**:

- `bool` - Test result

## Usage example on MicroPython

### Simple use

~~~python
# Import module
import localPTZtime

# Define the timestamp - this is 13 March 2023 06:30:00 in GMT time zone
timestamp = 1678689000

# Define the Posix Time Zone - this is for Europe/Rome
ptz_string = "CET-1CEST,M3.5.0,M10.5.0/3"

# Call tziso() function:
isotime = localPTZtime.tziso(timestamp, ptz_string)

# Print result
print(isotime)
~~~

Expected result is:
> 2023-03-13T07:30:00+01

The function tziso() can also be callable with a third parameter which, if set to `False`, disables the "zone designator" (`+01` in this example) as described here: https://en.wikipedia.org/wiki/ISO_8601#Time_zone_designators

### More advanced use

An example using NTP synchronization can be seen in the [_example.py](_example.py) file.
You will only need to set the Wi-Fi data and the definition string.

## Note

Posix TZ string like `<+11>-11` shouldn't be valid as defined on the [gnu.org](https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html) site, but they appear to be widely used. For this reason they are still accepted.

## Known issues

* No formal string checks can be performed in MicroPython at this time; Using a malformed string causes unpredictable errors.

## To Do

1. Enable use of checkptz() also in MicroPython. 
2. More test for various timezones and special cases. Tests for DST defined with "Jn" or "n" instead of "M".
