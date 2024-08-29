#! /usr/bin/env python3 
# Use 'python3 file_renamer.py' in Terminal or Command Line to execute script.

import os
import csv

source_path = "/Users/Dean/Documents/DPC_Python_Study_Group/Codedex_Projects/file_renamer"  # Change source_path as needed
file_list = os.listdir(source_path)

output_file = "renamed_files.csv"

# Open your CSV file in write mode
with open(output_file, "w", newline="") as csvfile:
    # Define your CSV's columns
    fieldnames = ["Old Filename", "New Filename"]
    # Initialize your CSV writer
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # Write the header to your CSV file
    writer.writeheader()

    # Iterate over the files in your directory
    for file in file_list:
        # Check if the file is a '.jpg' file and if 'foo' is in the filename. 
        # Script can be adapted to check for other file types and replacement targets.
        if file.endswith('.jpg') and 'foo' in file:
            # Generate the new name by replacing 'foo' with 'bar'. Script can be adapted to allow for other changes.
            new_name = file.replace('foo', 'bar')
            # Rename the file
            os.rename(os.path.join(source_path, file), os.path.join(source_path, new_name))
            # Write a row to your CSV file with the old and new filenames
            writer.writerow({"Old Filename": file, "New Filename": new_name})
