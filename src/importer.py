import glob
import csv

from datetime import datetime

RAW_DATABASE = "data/raw.csv"

def date_within_range(date, month, year):
    split_date = date.split("-")
    entry_month = int(split_date[1])
    entry_year = int(split_date[0])

    return (entry_month == month) and (entry_year == year)

def get_filenames(institution):
    return [f for f in glob.glob("data/" + institution + "/*.[c|C][s|S][v|V]")]

def import_amex(f, month, year, format):
    with open(f, "r") as file:
        reader = csv.reader(file)
        if (format == "new"):
            next(reader, None) # Skip header

        for lines in reader:
            if (format == "old"):
                date = lines[0].split("/")
                date = date[2] + "-" + date[0] + "-" + date[1]
                amount = lines[2].strip()
                description = lines[3]
            else:
                date = lines[0].split(" ")
                date = date[2] + "-" + str(datetime.strptime(date[1], '%b').month) + "-" + date[0]
                amount = lines[5].strip()
                description = lines[2]

            if date_within_range(date, month, year) == False:
                continue

            # Do not double count credit card expenses.
            if "PAYMENT RECEIVED" in description:
                continue

            with open(RAW_DATABASE, "a") as file:
                writer = csv.writer(file)
                row = [date, amount, "amex", description.upper()]
                writer.writerow(row)

def import_rogers(f, month, year):
    with open(f, "r") as file:
        reader = csv.reader(file)
        next(reader, None) # Skip header

        for lines in reader:
            if lines == []:
                continue

            date = lines[0]
            description = lines[7]

            if date_within_range(date, month, year) == False:
                continue

            # Do not double count credit card expenses.
            if "AUTO PAYMENT" in description or "CashBack" in description:
                continue

            if (year < 2023):
                amount = lines[11].replace("$", "")
            else:
                amount = lines[12].replace("$", "")

            with open(RAW_DATABASE, "a") as file:
                writer = csv.writer(file)
                row = [date, amount, "rogers", description.upper()]
                writer.writerow(row)

def import_tangerine(f, month, year):
    with open(f, "r") as file:
        reader = csv.reader(file)
        next(reader, None) # Skip header

        for lines in reader:
            date = lines[0].split("/")
            date = date[2] + "-" + date[0].zfill(2) + "-" + date[1].zfill(2)
            amount = lines[4]
            # Not interested in tracking income for the time being.
            if float(amount) >= 0:
                continue
            amount = amount[1:]
            # In rare cases, the Memo in column 3 provides necessary information.
            description = lines[2] + " " + lines[3]

            if date_within_range(date, month, year) == False:
                continue

            # Do not double count credit card expenses.
            if "ROGERS BANK" in description or "AMEX" in description or "ROYAL BANK VISA" in description:
                continue
            # Do not count reversed payments.
            if "Reversal" in description:
                continue

            with open(RAW_DATABASE, "a") as file:
                writer = csv.writer(file)
                row = [date, amount, "tangerine", description.upper()]
                writer.writerow(row)

def import_all_transactions(month, year):
    with open(RAW_DATABASE, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "amount", "bank", "description"])

    for file in get_filenames("amex-old-format"):
        import_amex(file, month, year, "old")
    for file in get_filenames("amex-new-format"):
        import_amex(file, month, year, "new")
    for file in get_filenames("rogers"):
        import_rogers(file, month, year)
    for file in get_filenames("tangerine"):
        import_tangerine(file, month, year)
