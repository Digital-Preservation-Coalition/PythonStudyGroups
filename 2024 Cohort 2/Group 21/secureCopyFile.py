#!/usr/bin/env python3

import os.path

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
source_path: str = './test_data/'
destination_path: str = './test_destination/'

full_source_path = source_path + name_of_file_to_be_copied

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
    print('Yes, the folder exists\n')
else:
    print('The folder does not exist. Exiting.\n')
    exit()
