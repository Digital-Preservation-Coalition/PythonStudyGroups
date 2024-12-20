#!/usr/bin/env python3

import os.path
import sys
import shutil

def get_script_directory():
    return os.path.dirname(os.path.realpath((sys.argv[0])))

def check_path_exists(path: str) -> bool:
    print('\n Checking for existence of "' + path + "'")
    return os.path.exists(path)

def check_file_has_data(file_path: str) -> bool:
    print('\n Checking file length')

    if os.path.getsize(file_path) > 0:
        return True
    else:
        return False

# Change these to test in your environment
name_of_file_to_be_copied: str = 'test_data1.txt'
source_path: str = get_script_directory() + '/test_data/'
destination_path: str = get_script_directory() + '/test_destination/'

full_source_path = source_path + name_of_file_to_be_copied
full_destination_path = destination_path + name_of_file_to_be_copied

print('The path where my test data is: ' + get_script_directory()  + '\n')

# Step 1: check if the file exists
if check_path_exists(full_source_path):
    print('Yes, the file exists\n')
else:
    print('The file does not exist. Exiting.\n')
    exit()

# Step 2: check if the file has data
if check_file_has_data(full_source_path):
   print ('The file has data\n')
else:
   print ('The file is empty. Exiting.\n')
   exit()

# Step 3: check if deestination path exists
if check_path_exists(destination_path):
    print('Yes, the destination folder exists\n')
else:
    print('The destination folder does not exist. Exiting.\n')
    exit()

# Step 4: check if file already exists
if check_path_exists(full_destination_path):
    print('Destination file already exists. Exiting.\n')
    exit()
else:
    print('File does not already exist in destination folder\n')

print('Ready to copy ' + full_source_path + ' to ' + full_destination_path + '.\n')

# Step 5: copy source file to destination folder
shutil.copy(full_source_path, full_destination_path)

# Step 6: see if destination file now exists
if check_path_exists(full_destination_path):
    print('Destination file copied.\n')
else:
    print('Destination file NOT copied. Exiting.\n')

# Step 7: check source and destination file sizes
src_file_size = os.path.getsize(full_source_path)
dest_file_size = os.path.getsize(full_destination_path)
if (src_file_size == dest_file_size):
    print('Source and destination files are the same size.  Copy successful.\n')
else:
    print('Source and destination file sizes are different.  Copy failed.\n')
