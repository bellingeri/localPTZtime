# ABOUT

This module allows the conversion of a timestamp with UTC timezone into other timezones expressed with the Posix Time Zone notation where other methods are not available.

No dependencies on 'date', 'calendar', etc. modules; only 'time' and 're'.

A description of the format can be found at these addresses:
* https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html
* https://www.postgresql.org/docs/current/datetime-posix-timezone-specs.html

A complete list of strings - and the code to generate them starting from the database maintained by IANA (https://www.iana.org/time-zones), present on linux systems - can be find at this address:
* https://github.com/nayarsystems/posix_tz_db

## Da fare

1. Test for various timezones and for special cases.
2. Micropython compatibility
3. Consider whether it is possible to remove the dependency on the 'time' module.