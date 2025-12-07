import csv
from pathlib import Path
from datetime import datetime

# Variables for the file paths:
main_file = Path("csv_files/main_youtube-subscriptions-2025-11-18.csv")     # Main file of subscriptions
sub_file = Path("csv_files/old_youtube-subscriptions-2025-10-18.csv")       # Older file I want to check for extra channels

def load_csv(file_path):
    """Read the .csv files as a function for less code repetition.
    UTF-8 encoding is used to handle different characters in the channel names (avoid errors)."""
    with file_path.open(newline="", encoding="utf-8") as f:
        return [row for row in csv.reader(f) if any(cell.strip() for cell in row)]

# Using the above function load both of the csv files:
main_list = load_csv(main_file)
main_header = main_list[0]
main_data = main_list[1:]
sub_list = load_csv(sub_file)[1:]   # the [1:] clause here makes the sub file list skip the header since we know it's the same (same file structure as main file)

# Convert lists of rows into sets of tuples for fast comparison:
# *Lists can't be in sets, so HAVE to be tuples
# **Sets are preferred over lists in comparison since it checks for content instead of looped checking (& index + pos)
main_set = {tuple(row) for row in main_data}
sub_set = {tuple(row) for row in sub_list}

# Performing the comparison operations:
matched_rows  = main_set & sub_set       # (Intersection) Rows that exist in both
main_extra_rows  = main_set - sub_set    # (Difference) Rows in Main CSV but not in sub CSV
sub_extra_rows   = sub_set - main_set    # (Difference) Reverse of above ^^

def write_csv():
    """A simple writer if sub_extra_rows is not empty.
    It adds main subs and sub extras into a list, sorts and writes into a new file. """
    if sub_extra_rows:

        combined_list = [list(row) for row in matched_rows] + [list(row) for row in sub_extra_rows]  # Add main list and the missing list to create a merged new file.
        combined_list.sort(key=lambda row: row[2].lower())   # Sort all entries by the 3rd "[0,1,2]" column, which is the channel name.

        today = datetime.today().strftime("%Y-%m-%d")   # Get today's date in format "2025-01-24"
        output_file = Path(f"csv_files/new_youtube-subscriptions-{today}.csv")  # Define what is an output file and where it goes

        with output_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(main_header)    # Write the header row first
            for row in combined_list:   # Write the individual data rows from the combined_list
                writer.writerow(row)

        print("\n=== OUTPUT: File generated, check csv_files. ===\n")

    else:
        print("\n=== OUTPUT: Nothing new to add, file not generated. ===\n")


# OUTPUT: -------------------------------------------------------------------------------------------------------------


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

write_csv()