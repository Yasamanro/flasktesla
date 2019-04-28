#!/usr/bin/env python
import csv
import sys

import flasktesla
# from flasktesla.models import User, Ride


def load_from_csv(filename):
	with open(filename, mode='r') as csv_file:
	    csv_reader = csv.DictReader(csv_file)
	    line_count = 0
	    for row in csv_reader:
	    	print(row)
	    	# Ride(row["id"],)
	     #    if line_count == 0:
	     #        print(f'Column names are {", ".join(row)}')
	     #        line_count += 1
	     #    print(f'\t{row["id"]} {row["date_of_ride"]} {row["start_lat"]} {row["start_lng"]} {row["end_lat"]} {row["end_lng"]} {row["avg_speed"]} {row["speed_limit"]}')
	     #    line_count += 1
	    print(f'Processed {line_count} lines.')
 

if __name__ == "__main__":
	load_from_csv(sys.argv[1])