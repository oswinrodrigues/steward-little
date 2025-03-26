import csv

SUMMARY_DATABASE = "data/summary.csv"

def summarize_expenses(month, year, dictionary, mode):
    # Hard code the order of the categories as they are in my spreadsheet
    # TODO: this will miss any new categories added - is there a better way to implement custom ordering?
    sorted_keys = ["giving", "saving", "rent", "utilities", "insurance", "recurring", "groceries", "transport", "health", "misc", "home", "restaurants", "relationships", "clothing", "recreation", "travel"]

    with open(SUMMARY_DATABASE, mode) as file:
        writer = csv.writer(file)

        if mode == "w":
            header = ["year", "month"]
            header.extend(sorted_keys)
            writer.writerow(header)

        row = [year, "{:02}".format(month)]
        row.extend([dictionary[key] for key in sorted_keys])
        writer.writerow(row)

def print_summary(dictionary):
    for entry in sorted(dictionary):
        print("{0:20} ${1:>10,.2f}".format(entry, dictionary[entry]))
