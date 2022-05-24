# steward-little
> "My money don't jiggle, jiggle. It folds." - Louis Theroux

An automated expense tracker for personal finance stewardship. Here's how it works:
1. Read all bank and credit card statements (CSV) from `data/` for a specific month.
2. Consolidate and standardize these entries into a new `data/raw.csv` file.
3. Run the entries in `raw.csv` against those in `data/categories/`.
   1. If there's a match, assign that category to the expense item in question.
   2. If there's no match, prompt the user for a category. Update the associated category file, too.
   3. If there's a match with a multi-category merchant (e.g. Amazon), prompt the user for a category for that specific purchase.
4. Import the categorized data into a Notion database, for better processing & visualization.
   1. User can manually import the categorized CSV into their Notion database.
   2. Script can use the Notion API to push each data point to a specified database.
