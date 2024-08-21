## rssharvester.py
- written for Python 3.12.1
- requires user to provide a URL to an rss feed for a podcast
- creates a csv in the same location where the script is saved; file contains all rss data where each row is one episode
- column headers are labelled with the Dublin Core metadata element used in the UDC
- cells will require cleanup and review before they're ready to do anything with
- to download images and audio files, I use Chrome extensions to bulk open URLs in new tabs and to bulk download
- known issues:
  -  resulting metadata requires substantial cleanup that could be minimized in the code (e.g., parsing attachment data to return only URLs rather than the whole tag)
  -  may not work if rss feed doesn't meet common syndication requirements (e.g., apple podcasts)
  -  in-script reporting is minimal and could be improved

## filepath-validator.py
- written for Python 3.12.1
- requires user to provide EITHER a CSV file (with a list of filepaths/filenames in column A) OR a starting directory (which the script searches recursively to create a file list)
- checks each file for...
  -  a well-formed extension (a period with 3 characters)
  -  one and only one period
  -  no whitespace or nonprinting characters
  -  characters outside of a-z, A-Z, 0-9, dash, underscore, backslash, and period
  -  0 or 1 colon (allow for relative and absolute filepaths)
- creates a csv in the same location where the script is saved; file contains the file list as well as each potential issue in its own column (e.g., extension issues are noted in column B and whitespace issues are noted in column C).
- known issues: 
  -  may return false positives for accepted 4-character extensions (e.g., JPEG or TIFF)

## csv-rename-and-move.py
- written for Python 3.12.1
- requires a CSV with a current filepath and filename in column A, and a desired filepath/filename in column B
- checks that the new path/filename isn't already taken and checks each new path/name for quality (see filepath-validator.py)
- skipping any of those potential problems, it will create any directories that are needed and move/rename files
- gives a summary of files found, successes, and errors
- creates a log with a file-by-file summary of changes
