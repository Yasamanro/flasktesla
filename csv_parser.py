#!/usr/bin/env python
import csv
import sys

from flasktesla.models import User, Ride
from flasktesla import db
from time import strptime
from datetime import datetime


def load_from_csv(filename):
	with open(filename, mode='r') as csv_file:
		session = db.session()
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		for record in csv_reader:
			del record['id']
			record['date_of_ride'] = datetime.strptime(record['date_of_ride'], '%Y-%m-%d %H:%M:%S.%f')
			r = Ride(**record)
			session.add(r)

		print(f'Processed {line_count} lines.')

		session.commit()

if __name__ == "__main__":
	load_from_csv(sys.argv[1])