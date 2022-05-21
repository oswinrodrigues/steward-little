import csv
import os

CATEGORY_PATH = "data/categories"

def get_categories():
    return [file.strip(".txt") for file in os.listdir(CATEGORY_PATH)]

def find_category(description):
    for category in get_categories():
        with open(f"{CATEGORY_PATH}/{category}.txt", "r") as file:
            for line in file:
                if line[:-1] in description: # Ignore line ending
                    return category
    return None # No category found for this description

def request_category(description):
    enumeration = {i: c for i, c in enumerate(get_categories())}

    print(f"Please specify a category for: {description}")
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
        file.write(description)

MASTER_DATABASE = "data/master.csv"
RESULTS_FILE = "data/master_categorized.csv"

def categorize_expenses():
    with open(MASTER_DATABASE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"] == "date":
                continue # Skip header row

            description = row["description"]
            category = find_category(description)
            if category is None:
                category = request_category(description)
                add_to_category(description, category)

            row["category"] = category

            with open(RESULTS_FILE, "a") as results:
                writer = csv.DictWriter(results, fieldnames=row.keys())
                writer.writerow(row)
