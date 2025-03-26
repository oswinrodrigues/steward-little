# steward-little
> "My money don't jiggle, jiggle. It folds." - Louis Theroux

An automated expense tracker for personal finance stewardship. Here's how it works:
1. Read all bank and credit card statements (CSV) from `data/` for a specific month.
2. Consolidate and standardize these entries into a `data/raw.csv` file.
3. Run the entries in `data/raw.csv` against those in `data/categories/`.
   1. If there's a match, assign that category to the expense item in question.
   2. If there's no match, prompt the user for a category. Update the associated category file, too.
4. Write categorized and/or summarized entries to CSV files or Notion database, depending on user choice.

## Requirements
Due to the Notion integration, the program requires:
   - The Python module `requests`. Install it with the command `python -m pip install requests`
   - A `src/secret.py` file that defines the constants `SECRET_TOKEN` and `NOTION_DATABASE`

## Command Structure
```
python src/main.py [o={csv,notion}] [m=<month>] [y=<year>]
```
