
import os
dir_path = r'/home/ns/psg/files'
os.chdir(dir_path)

def remove_unwanted_files(unwanted_file):
    """ Recursively remove unwanted files from a directory.

    More detailed documentation.
    """
    flag = 0
    for root, dirs, files in os.walk(dir_path):
        os.chdir(root)
        for file in files:
            if file == unwanted_file:
                print('Found file ' + file + " in directory " + dir_path)
                os.remove(file)
                print('File removed')
                flag = 1
    if flag == 0:
        print("Sorry, did not find file " + unwanted_file + " in directory " + dir_path)

def main():
    try:
        remove_unwanted_files(sys.argv[1])
    except IndexError:
        print("Usage:\n", sys.argv[0], "Name_of_unwanted_file")

if __name__ == "__main__":
    import sys
    sys.exit(main())
