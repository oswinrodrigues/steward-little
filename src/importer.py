import os
import glob
import csv

def get_filenames(institution):
    path = os.getcwd().split("steward-little")[0]
    return [f for f in glob.glob(path + "steward-little/data/" + institution + "/*.csv")]

def import_amex(filenames, master):
    for f in filenames:
        with open(f, 'r') as file:
            reader = csv.reader(file)

            for lines in reader:
                date = lines[0]
                amount = lines[2].strip()
                description = lines[3]

                # Do not double count credit card expenses.
                if "PAYMENT RECEIVED" in description:
                    continue

                master.append([date, amount, description])
    return master

def import_rogers(filenames, master):
    for f in filenames:
        with open(f, 'r') as file:
            reader = csv.reader(file)
            next(reader, None) # Skip header

            for lines in reader:
                date = lines[0].split('-')
                new_date = date[1] + "/" + date[2] + "/" + date[0]
                amount = lines[11].replace('$', '')
                description = lines[7]

                # Do not double count credit card expenses.
                if "AUTO PAYMENT" in description or "CashBack" in description:
                    continue

                master.append([new_date, amount, description])
    return master

def import_tangerine(filenames, master):
    for f in filenames:
        with open(f, 'r') as file:
            reader = csv.reader(file)
            next(reader, None) # Skip header

            for lines in reader:
                date = lines[0]
                amount = lines[4]
                # Not interested in tracking income for the time being.
                if float(amount) >= 0:
                    continue
                new_amount = amount[1:]
                # In rare cases, the Memo in column 3 provides necessary information.
                description = lines[2] + " " + lines[3]

                # Do not double count credit card expenses.
                if "ROGERS BANK" in description or "AMEX" in description or "ROYAL BANK VISA" in description:
                    continue
                # Do not count reversed payments.
                if "Reversal" in description:
                    continue

                master.append([date, new_amount, description])
    return master

MASTER_DATABASE = "data/master.csv"

def write_master_transactions(master):
    path = os.getcwd().split("steward-little")[0]
    destination = path + "steward-little/" + MASTER_DATABASE
    fields = ['date', 'amount', 'description']
    with open(destination, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        writer.writerows(master)

def import_all_transactions():
    amex_filenames = get_filenames("amex")
    rogers_filenames = get_filenames("rogers")
    tangerine_filenames = get_filenames("tangerine")

    master = []
    master = import_amex(amex_filenames, master)
    master = import_rogers(rogers_filenames, master)
    master = import_tangerine(tangerine_filenames, master)

    write_master_transactions(master)
