#!/usr/bin/env python3

import categorizer
import importer
import sys

from calendar import month_name
from datetime import datetime

def is_month_valid(input):
    try:
        month = int(input)
    except ValueError:
        print("Please input a valid month index [1-12].")
        return False

    if (month < 1 or month > 12):
        print("Please input a valid month index [1-12].")
        return False

    return True

def is_year_valid(input):
    try:
        year = int(input)
    except ValueError:
        print("Please input a valid year.")
        return False

    if (year < 1):
        print("Please input a valid year.")
        return False

    return True

if __name__ == "__main__":
    month = datetime.now().month
    month_valid = True
    if len(sys.argv) > 1:
        if is_month_valid(sys.argv[1]) == True:
            month = int(sys.argv[1])
        else:
            month_valid = False

    year = datetime.now().year
    year_valid = True
    if len(sys.argv) > 2:
        if is_year_valid(sys.argv[2]) == True:
            year = int(sys.argv[2])
        else:
            year_valid = False

    if (month_valid == True) and (year_valid == True):
        destination = "data/{}{}.csv".format(month_name[month].lower(), year)

        importer.import_all_transactions(month, year)
        categorizer.categorize_expenses(destination)

        print("Categorized transactions for {} {} stored in {}".format(month_name[month], year, destination))
