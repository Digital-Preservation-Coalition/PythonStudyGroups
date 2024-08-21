#import necessary libraries
import csv
import re
import os

#determine starting input (directory or csv file list)
styleinput=input('Would you like to run this script by providing a starting directory, or by providing a CSV file list?  Enter "D" for directory or "F" for file list:')
if styleinput in ('D','d'):
    #get starting directory from user, validate, create a recursive file list
    dirinput=input('Starting directory: ')
    if os.path.isdir(dirinput)==False:
        print()
        print('PROBLEM WITH STARTING DIRECTORY! It looks like',dirinput,'is not a valid location. Please make sure your file path is complete and does NOT end with a final slash, and then re-run this script.')
        quit()
    else:
        filelist=[]
        def list_files_recursive(path='.'):
            for entry in os.listdir(path):
                filepath = os.path.join(path, entry)
                if os.path.isdir(filepath):
                    list_files_recursive(filepath)
                else:
                    filelist.append(filepath)
        list_files_recursive(dirinput)
elif styleinput in ('F','f'):
    #get filepath to CSV from user, establish output filename
    csv_input = input("Enter the filepath and name of the input CSV: ")
    filelist=[]
    with open(csv_input, mode='r', encoding="utf8", errors='ignore') as userinput:
        reader = csv.DictReader(userinput)
        for line in userinput:
            filepath=line.rstrip(',\n')
            filelist.append(filepath)
else:
    print()
    print('PROBLEM WITH YOUR INPUT!  Re-run this script, and be sure to enter "D" to use a starting directory or "F" to start with a CSV file list.')
    quit()

#set up counters
issuecount=0
filecount=0

#create output log, write header row
csv_output = input("This script creates a CSV log that provides detailed information on each file.  Enter the filepath and filename where you would like the log to be saved:")
with open(csv_output, mode='w', newline='', encoding="utf8", errors='ignore') as outputlog:
    writer = csv.writer(outputlog, delimiter=',')
    writer.writerow(['File', 'Extension','Whitespace','Periods','Special Characters'])


#iterate through file list
for filepath in filelist:
    filecount=filecount+1
    charissue=''

    #check for a valid extension format
    extension=filepath[filepath.rfind("."):]
    if re.search(r'[.]\S\S\S$',extension):
        extissue=''
    else:
        issuecount=issuecount+1
        extissue='improper extension format'

    #check for spaces and nonprinting characters
    whitespacematches=re.findall(r'\s',filepath)
    if len(whitespacematches)>0:
        issuecount=issuecount+1
        whitespaceissue='contains spaces or nonprinting characters'
    else:
        whitespaceissue=''
    
    #check for multiple periods
    periodmatches=re.findall(r'[.]',filepath)
    if len(periodmatches)>1:
        issuecount=issuecount+1
        periodissue='contains multiple periods'
    else:
        periodissue=''

    #check 0 or 1 colons
    colonmatches=re.findall(r'[:]',filepath)
    if len(colonmatches)>1:
        issuecount=issuecount+1
        charissue='contains special characters'
    else:
        charissue=charissue

    #check for invalid characters
    invalidcharmatches=re.findall(r'[^a-zA-Z0-9._\\\-: ]',filepath)
    if len(invalidcharmatches)>0:
        issuecount=issuecount+1
        charissue='contains special characters'
    else:
        charissue=charissue

    #combine issue text, write row to log
    itemlog=[filepath,extissue,whitespaceissue,periodissue,charissue]
    with open (csv_output, mode='a',encoding="utf8", newline='',errors='ignore') as outputlog:
        writer = csv.writer(outputlog)
        writer.writerow(itemlog)

print('PROCESS FINISHED.')
print(filecount,' files checked')
print(issuecount,' issues found')
print('Check the log for details: ',csv_output)