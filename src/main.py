#!/usr/bin/env python3

import importer

import os
import csv
import sys

import calendar
from datetime import datetime

def display_month_expenses(month, year):
    # TODO: update with real categories
    categories = ['Gas', 'Restaurants', 'Recurring', 'Clothing', 'Misc']
    sums = {key: 0.00 for key in categories}
    entries = {key: [] for key in categories}

    path = os.getcwd().split("steward-little")[0]
    destination = path + "steward-little/data/master.csv"
    at_least_one_entry = False
    with open(destination, 'r') as file:
            reader = csv.reader(file)
            next(reader, None) # Skip header

            for lines in reader:
                date = lines[0].split('/')
                entry_month = int(date[0])
                entry_year = int(date[2])
                if (entry_month != month) or (entry_year != year):
                    continue

                at_least_one_entry = True
                category = lines[3]
                amount = float(lines[1])
                sums[category] += amount
                entries[category].append(lines)

    month_string = calendar.month_name[month]
    if (at_least_one_entry == True):
        print(month_string.upper(), year)
        for c in categories:
            print(' {}: ${}'.format(c, sums[c]))
            for entry in entries[c]:
                print('    {} ${}\t{}'.format(entry[0], entry[1], entry[2]))
    else:
        print('No expenses found for {} {}.'.format(month_string, year))

if __name__ == "__main__":
    #importer.import_all_transactions()

    if len(sys.argv) == 1:
        month = datetime.now().month
    else:
        # TODO: verify input
        month = int(sys.argv[1])

    year = datetime.now().year

    display_month_expenses(month, year)
