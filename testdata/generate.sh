#!/bin/bash
#
# Generate A LOT OF testdata and save it to testdata.tsv
# (tab separated values).

set -eu

export TZ="CET-1CEST,M3.5.0,M10.5.0/3"

UNIXTIME=$(date -d 2000-01-01T12:00Z +%s)
UNIXTIME_MAX=$(date -d 2050-01-01T12:00Z +%s)

rm -f testdata.tsv

while [[ $UNIXTIME -le $UNIXTIME_MAX ]] ; do
	LOCAL=$(date -d @$UNIXTIME -Iseconds)
	echo "$TZ	$UNIXTIME	$LOCAL" >> testdata.tsv

	let UNIXTIME+=86400
done
