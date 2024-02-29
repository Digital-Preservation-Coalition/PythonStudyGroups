#!/usr/bin/env python3

# For Mac, use normal forward slashes
# source_path = "/Users/sonic/Pictures/test"

import os

source_path = "/Users/sonic/Pictures/test"  # Change as per your OS
file_list = os.listdir(source_path)
print(file_list)

for file in file_list:
    # Check if the file ends with '.jpg'
    if file.endswith('.jpg'):
        # Check if 'foo' is in the file name
        if 'foo' in file:
            # Replace 'foo' with 'bar' in the file name
            new_name = file.replace('foo', 'bar')
            # Rename the file using os.rename
            os.rename(os.path.join(source_path, file), os.path.join(source_path, new_name))
            # Print out a confirmation message
            print(f"Renamed {file} to {new_name}")  # Expected output: Renamed foo_0001.jpg to bar_0001.jpg
        if 'bar' in file:
            new_name = file.replace('bar', 'done')
            os.rename(os.path.join(source_path, file), os.path.join(source_path, new_name))
            print(f"Renamed {file} to {new_name}")