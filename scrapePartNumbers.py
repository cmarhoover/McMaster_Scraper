# This script processes a text file to extract specific part numbers and save them to a CSV file.
# It works by:
# 1. Reading a text file (ExampleNutList.txt) containing various data.
# 2. Using a regular expression to search for part numbers in the text, where part numbers 
#    follow a pattern like "95462A029" (a series of digits followed by a letter and more digits).
# 3. Extracting all matching part numbers and writing them into a CSV file (PartNumbers.csv) 
#    with one part number per row.
# 4. It also prints the total number of part numbers found in the text file for reference.

import re
import csv

# Path to the input and output files
input_file_path = 'ExampleNutList.txt'
output_file_path = 'PartNumbers.csv'

# Open and read the input file
with open(input_file_path, 'r') as file:
    content = file.read()

# Regular expression to match part numbers like "95462A029"
part_number_pattern = r'\b\d+[A-Z]\d+\b'

# Find all part numbers in the file
part_numbers = re.findall(part_number_pattern, content)

# Write the part numbers to a CSV file
with open(output_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Part Number'])  # Write the header
    for part_number in part_numbers:
        csvwriter.writerow([part_number])

# Print the number of part numbers found
print(f'Total part numbers found: {len(part_numbers)}')
