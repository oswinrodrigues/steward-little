import csv
import os

CATEGORY_PATH = "data/categories"
RAW_DATABASE = "data/raw.csv"

def get_categories():
    return [file.split(".")[0] for file in os.listdir(CATEGORY_PATH)]

def find_category(description):
    for category in get_categories():
        with open(f"{CATEGORY_PATH}/{category}.txt", "r") as file:
            for line in file:
                if line[:-1] in description: # Ignore line ending
                    return category
    return None # No category found for this description

def request_category(description, amount):
    enumeration = {i: c for i, c in enumerate(get_categories())}

    print(f"Please specify a category for: {description} (${amount})")
    print(f"Either enter a number for an existing category: \n{enumeration}")
    print("Or enter a new category name to be added to the list!")

    selection = input("Enter selection: ")
    try:
        selection = int(selection)
        if selection in enumeration.keys():
            return enumeration[selection] # Existing category
    except ValueError: # Cannot convert string to integer
        return selection # New category

def add_to_category(description, category):
    # Need "a+" mode in case the category is new and the file DNE
    with open(f"{CATEGORY_PATH}/{category}.txt", "a+") as file:
        file.write(description + "\n")

def categorize_expenses(destination):
    with open(RAW_DATABASE, "r") as file:
        reader = csv.DictReader(file)

        with open(destination, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "amount", "bank", "description", "category"])

        for row in reader:
            amount = row["amount"]
            description = row["description"]
            category = find_category(description)
            if category is None:
                category = request_category(description, amount)
                add_to_category(description, category)

            row["category"] = category

            with open(destination, "a") as results:
                writer = csv.DictWriter(results, fieldnames=row.keys())
                writer.writerow(row)

