# DPC Python ‘How-To’ Guide

# Deleting Thumbs.db Files

When working with a large digital collection or new accession, they can often be scattered with hundreds of redundant system files, such as ‘Thumbs.db’, not only do we not want to preserve these files, they can create bugs in our workflows and cause problems if ingested in to digital preservation systems, so it can be fairly useful to just delete them all in bulk. Fortunately this is something that can be done with only a few lines of Python code.

Even if this example isn’t relevant for your workflow, a lot of the concepts are transferrable to other tasks related to working with large numbers of files

### Import the OS module

Python modules are reusable sections of Python code that can be imported in to our scripts to give them more functionality for specific tasks, the OS module is incredibly powerful as it allows us to interact with files and directories on our system, this is particularly useful for Digital Preservation as we spend a lot our time working with lots of files

The module needs to imported at the top of your script like this 

```python
import os
```

### Define your directory path as a variable

The next thing we need to do is save the path of our desired directory in to the script, we can do this by saving it as a **variable**

Variables are one the most basic elements of programming. They are placeholders used to store data so that it can be easily accessed and manipulated throughout our script

Variables can store anything, but here the datatype of our path variable will be a **string** (a string of text). In Python this is indicated by it being surrounded in quotation marks (either `“` or `‘` )

You can name your variable anything you like, but it’s good practice to find the middle ground between making it clear what the variable refers to, but keeping the name short. 

It is also good practice to replace spaces with underscores in variable names, known as **snake case**

So for our directory path we’ll go with `dir_path`

This path should be the absolute path to your directory (full length including drive name)

When we’re working with directory paths in Python, we need to define them as a **raw string**. This is because paths contain backslashes, and in Python a backslash would usually indicate an **escape character**, (a character that instructs the code to behave differently, eg creating a newline). As we want our code to read the backslashes as actual backslashes, we need to prefix the string with a lower case r  

```python
import os

dir_path = r'path\to\files'
```

### Change working directory

The next thing we need to do is change our **working directory** to the directory that we defined earlier.

This means that any code we run will default to being run in this directory without having to have it’s full path ****specified. It is possible to avoid this step and use **absolute paths,** However doing it this way (**relative paths**) makes our code cleaner and easier to read as we get to grips with how these functions works

For this we’ll use the `os.chdir()` function. It starts with `os` as it comes from the `os` module, and the `chdir` means change directory. 

The parenthesis are where we place our **arguments**, the parameters for our function, `chdir` only takes one argument, the path of the directory we want to starting working in

```python
import os

dir_path = r'path\to\files'

os.chdir(dir_path)
```

### Iterate over your directory

The function from the OS module we’re going to use for this version of our script is `os.listdir()`

 `listdir` means list directory, this function returns a **list** containing everything in that directory. `listdir` only takes one argument, the path of the directory we want to list the contents of, however by default is uses the current working directory, which we changed in the line above

The output from us running the `os.listdir(dir_path)` is a list, but as we want to act on each element of the list we need to place it in a **for loop**, this will allow us to iterate over each item in our folder and execute our code on every item

The code underneath is what gets executed on each item, this is where we can perform actions on each file as it gets looped over, we’ll keep it simple for now and just print the name to the terminal 

```python
import os

dir_path = r'path\to\files'

os.chdir(dir_path)

for item in os.listdir():
	print(item)
```

You should now be able to run this code and have it print everything in that folder, one line at a time, in your terminal

You may have noticed that if you had any sub-folders in that folder, they’d have shown up here too. But what if you only wanted to see the files? 

We can add a conditional **`if`** statement so that our code will only return files

Here we use the `os.path.isfile()` function, as before we pass an argument in to the parenthesis of the function, this time it’s the item. However this time the function returns a **boolean** value (True or False) based whether the item is a file or not. If it’s a file then the code continues to the line underneath. In this case the print statement.

```python
import os

dir_path = r'path\to\files'

os.chdir(dir_path)

for item in os.listdir():
	if os.path.isfile(item):
		print(item)
```

<aside>
💡 TIP: If you wanted to do the opposite and only return folders, you can use `os.path.isdir()`

</aside>

## Find the Thumbs.db files

Now we have that set up, we can easily modify it to search for and remove the Thumbs.db files

The first thing we need to do is add another conditional `if` statement to check the name of the file, using the **comparison operator** `==`

```python
import os

dir_path = r'path\to\files'

os.chdir(dir_path)

for item in os.listdir():
	if os.path.isfile(item):
		if item == 'Thumbs.db':
			print(item)
```

This will print any Thumbs.db files in the folder to the terminal

We are now ready to add a function, also from the **os** module, that will delete the files

```python
import os

dir_path = r'path\to\files'

os.chdir(dir_path)

for item in os.listdir():
	if os.path.isfile(item):
		if item == 'Thumbs.db':
			print(item)
			os.remove(item)
```

Running this now will delete those files from the folder

<aside>
💡 If you wanted to search for and delete a different type of file, such as *desktop.ini*, then all you’d need to do is modify the string in the comparison operator in line 7

</aside>

## Using os.walk to access more directories

So the example above could be useful if you have one single folder with a lot of those files inside it, but what if you had a huge collection with lots of sub-folders and you wanted to remove all the Thumbs.db without having to check if they were there and where they were?

For this we can use `os.walk()`

`os.walk()` is fairly similar to `os.listdir()` except it works recursively. So any time it sees a folder, it will enter that folder and return what ever is inside it too

This is really useful as it means we can access any file or folder that sits under our top directory no matter how deep it’s nested

`os.walk()` **yields** 3 elements in a **tuple**, but the common practice is to unpack them with variable names ‘*root, dirs* and *files*’. *root* is a string of the directory path, and *dirs* and *files* are **lists** of all the sub directories and files in that root directory respectively

As it is recursive, it then goes through each of those sub directories in turn, and treats them as the root directory, and performs the same, this is how we can use it to access every single file even if it’s a very large set of folders

```python
import os

dir_path = r'path\to\files'

os.chdir(dir_path)

for root, dirs, files in os.walk(dir_path):
	print(root, dirs, files)
```

To access every file individually, we need to add a **nested for loop** underneath our first for loop. This will take the list of files that’s generated from each sub-folder, and retrieve every file within in

```python
import os

dir_path = r'path\to\files'

for root, dirs, files in os.walk(dir_path):
	for file in files:
		print(root, file)
```

After that we can perform actions on each file in the same way as before, with a small change.

In the `os.listdir()`example, we changed our working directory to the path in the dir_path variable. However when using `os.walk()` we need to iteravely change our working directory as we work our way through the sub-folders. To do this we change our working directory to the root variable, inside our first for loop. After that, we can add the same code as before for identifying and deleting the files we want to remove

```python
import os

dir_path = r'path\to\files'

for root, dirs, files in os.walk(dir_path):
	os.chdir(root)
	for file in files:
		if file == 'Thumbs.db':
			print(file)
			os.remove(file)
```

---