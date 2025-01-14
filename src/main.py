#!/usr/bin/env python3

import categorizer
import importer
import publisher
import summarizer
import sys

from calendar import month_name
from datetime import datetime

def is_month_valid(input):
    try:
        month = int(input)
    except ValueError:
        print("Please input a valid month index {1-12}.")
        return False

    if (month < 1 or month > 12):
        print("Please input a valid month index {1-12}.")
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
    year = datetime.now().year
    output = "csv"

    input_valid = True

    for arg in sys.argv[1:]:
        prefix = arg[0:2]
        value = arg[2:]
        if prefix == "m=":
            if is_month_valid(value) == True:
                month = int(value)
            else:
                input_valid = False
        elif prefix == "y=":
            if is_year_valid(value) == True:
                year = int(value)
            else:
                input_valid = False
        elif prefix == "o=":
            if value == "csv" or value == "notion":
                output = value
            else:
                print("Please input a valid output format {csv,notion}.")
                input_valid = False
        else:
            print("main.py [o={csv,notion}] [m=<month>] [y=<year>]\n")
            print("   Defaults:\n")
            print("      o=csv")
            print("      m=<current month>")
            print("      y=<current year>")
            input_valid = False
            break

    if (input_valid == True):
        destination = "data/{}{}.csv".format(month_name[month].lower(), year)

        importer.import_all_transactions(month, year)
        totals = categorizer.categorize_expenses(destination)

        if (output == "csv"):
            # Change "w"rite mode to "a"ppend mode if you want to build a summary for the year
            summarizer.summarize_expenses(month, year, totals, "w")
            print("Categorized transactions for {} {} written to {}".format(month_name[month], year, destination))
            print("Summarized transactions for {} {} written to data/summary.csv".format(month_name[month], year))
            print()
        else:
            publisher.publish_transactions(destination)
            print("Categorized transactions for {} {} published to Notion!".format(month_name[month], year))
            print()
