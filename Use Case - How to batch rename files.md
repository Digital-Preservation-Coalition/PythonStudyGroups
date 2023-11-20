# Python Script for Renaming Files

This guide outlines the creation of a Python script to rename files in a folder, specifically changing 'foo' in filenames to 'bar'.
As this involves changing the names of files, it is advisable to run this script on test files.

## Overview of Steps Python Will Perform

1. **Create a Blank Python Script**: Start with an empty script called `renamer.py`.
2. **Identify the Folder**: Specify which folder you want to process.
3. **List Files in the Folder**: Generate a list of files in the specified folder.
4. **Filter Relevant Files**: Focus on files that end with 'jpg' and contain 'foo' in their names.
5. **Rename Files**: Replace 'foo' with 'bar' in the filenames.
6. **Provide Feedback**: Output a status report indicating the renaming process.

## Prior Knowledge Required

- Basic understanding of Python syntax.
- Familiarity with loops, if statements, and error handling.
- How to import and use Python libraries.
- Working with a filesystem in a command-line interface.
  
### Create a Blank Python Script

Create a new Python script named `renamer.py`. Use a text editor for this, and save it in a convenient location, such as your home directory (C:/Users/$USERNAME on Windows, /Users/$USERNAME on Mac). 

Include a shebang at the top of the script for ease of running it in the terminal:

```python
#!/usr/bin/env python3
```

### Specify the Folder to Process

Declare a variable in your script to specify the folder you want to process. Here's how you can do it for both Windows and Mac:
In this example, the user account for Windows or Mac is 'Best Programmer', but replace it with whatever your username is.

```python
#!/usr/bin/env python3

# For Windows, use double backslashes and enclose the path in quotes
source_path = "C:\\Users\\Best Programmer\\Documents\\Photos"

# For Mac, use normal forward slashes
# source_path = "/Users/BestProgrammer/Documents/Photos"
```

We will use the Windows example for the rest of this script, but replace it with the Mac path if required.
### Generate a List of All Files in the Folder

Using `os.listdir`, create a list of files in `source_path`.
In order to use `listdir`, we must import the `os` module at the top of the script.

```python
#!/usr/bin/env python3
import os

source_path = "C:\\Users\\Best Programmer\\Documents\\Photos"  # Change as per your OS
file_list = os.listdir(source_path)
```

### Debug: Verify File List Creation and Run the Script

For debugging, add a print statement to check the list of files. At this point, you should run the script to ensure it's working correctly. Here's how to run it:

- Open your terminal or command prompt.
- Navigate to the directory where `renamer.py` is located.
- Run the script by typing `python renamer.py` or `python3 renamer.py` (depending on your Python installation).

```python
#!/usr/bin/env python3
import os

source_path = "C:\\Users\\Best Programmer\\Documents\\Photos"  # Change as per your OS
file_list = os.listdir(source_path)
print(file_list)
```

The expected output should be the list of files, for example:
`['foo_0001.jpg', 'document.pdf', 'foo_0002.jpg']`

### Filter and Rename Files: Explanation

In this section, we will filter the files that meet our criteria (ending with 'jpg' and containing 'foo') and then rename them.

```python
#!/usr/bin/env python3
import os

source_path = "C:\\Users\\Best Programmer\\Documents\\Photos"  # Change as per your OS
file_list = os.listdir(source_path)

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
```

- `file.endswith('.jpg')`: Checks if a file name ends with the '.jpg' extension.
- `'foo' in file`: Determines if the string 'foo' is part of the file name.
- `file.replace('foo', 'bar')`: Creates a new string where 'foo' is replaced with 'bar'.
- `os.rename(...)`: Tells the operating system to rename the file from its old name to the new name.
- `os.path.join(...)`: Combines the directory path with the file name to create a full file path.

- Run the script by typing `python renamer.py` or `python3 renamer.py` (depending on your Python installation).

### Conclusion and Additional Steps

- Input for the directory path can be added using `sys.argv[1]` or `argparse`.
- Recursive processing in subdirectories using `os.walk()`.
- Implementing a dry run mode.
- Creating logs for file changes.


