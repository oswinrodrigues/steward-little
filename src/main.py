#!/usr/bin/env python3

import importer
import categorizer

if __name__ == "__main__":
    importer.import_all_transactions()
    categorizer.categorize_expenses()
