import csv

main_file = 'csv_files/main_youtube-subscriptions-2025-11-18.csv'
sub_file = 'csv_files/old_youtube-subscriptions-2025-10-18.csv'

main_list = []
sub_list = []
missing_list = []

with open(main_file, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        main_list.append(row)

with open(sub_file, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        sub_list.append(row)

print(f"Main list:\n{main_list}\n")
print(f"Sub list:\n{sub_list}\n")

for item in sub_list:
    if item in main_list:
        print(f"MATCHED: {item}")
    if item not in main_list:
        missing_list.append(item)
        print(f"UNMATCHED: {item}")

print(f"\nNon-matched list:\n{missing_list}")
