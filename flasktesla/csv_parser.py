#!/usr/bin/env python
import csv


def load_from_csv(filename):
	with open(filename, mode='r') as csv_file:
	    csv_reader = csv.DictReader(csv_file)
	    line_count = 0
	    for row in csv_reader:
	        if line_count == 0:
	            print(f'Column names are {", ".join(row)}')
	            line_count += 1
	        print(f'\t{row["id"]} {row["department"]}, and was born in {row["birthday month"]}.')
	        line_count += 1
	    print(f'Processed {line_count} lines.')
 

if __name__ == "__main__":
	load_from_csv()