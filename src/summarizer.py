import csv

SUMMARY_DATABASE = "data/summary.csv"

def summarize_expenses(month, year, dictionary, mode):
    sorted_keys = sorted(dictionary.keys())

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
