This module allows the conversion of a timestamp with UTC timezone into other timezones expressed with the Posix Time Zone notation where other methods are not available.

A description of the format can be found at these addresses:
https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html
https://www.postgresql.org/docs/current/datetime-posix-timezone-specs.html

You can find a complete list of strings - and the code to generate them starting from the database maintained by IANA (https://www.iana.org/time-zones), present on linux systems - at this address:
https://github.com/nayarsystems/posix_tz_db