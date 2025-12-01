import csv
from pathlib import Path

# Variables for the file paths:
main_file = Path("csv_files/main_youtube-subscriptions-2025-11-18.csv")     # Main file of subscriptions
sub_file = Path("csv_files/old_youtube-subscriptions-2025-10-18.csv")       # Older file I want to check for extra channels

def load_csv(file_path):
    """Read the .csv files as a function for less code repetition.
    UTF-8 encoding is used to handle different characters in the channel names (avoid errors)."""
    with file_path.open(newline="", encoding="utf-8") as f:
        return [row for row in csv.reader(f)]

# Using the above function load both of the csv files:
main_list = load_csv(main_file)
sub_list = load_csv(sub_file)

# Convert lists of rows into sets of tuples for fast comparison:
# *Lists can't be in sets, so HAVE to be tuples
# **Sets are preferred over lists in comparison since it checks for content instead of looped checking (& index + pos)
main_set = {tuple(row) for row in main_list}
sub_set = {tuple(row) for row in sub_list}

# Performing the comparison operations:
matched_rows  = main_set & sub_set       # (Intersection) Rows that exist in both
main_extra_rows  = main_set - sub_set    # (Difference) Rows in Main CSV but not in sub CSV
sub_extra_rows   = sub_set - main_set    # (Difference) Reverse of above ^^

# Output:
print("\n=== MATCHED subs ===")
if not matched_rows:
    # If not checks, if the set is empty - if yes it prints "none"
    print("--none--")
else:
    for row in sorted(matched_rows):
        print(row)

print("\n=== Main extra (in Main but not in Sub CSV) ===")
if not main_extra_rows:
    print("--none--")
else:
    for row in sorted(main_extra_rows):
        print(row)

print("\n=== Sub extra (in Sub but not in Main CSV) ==="
      "\nTHIS IS WHAT WERE LOOKING FOR")
if not sub_extra_rows:
    print("--none--")
else:
    for row in sorted(sub_extra_rows):
        print(row)