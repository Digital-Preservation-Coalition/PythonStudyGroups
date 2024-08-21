#import necessary libraries
import os
import csv
import re

#get filepath to CSV from user
print()
print('Welcome!  This script will help you organize and rename files quickly and easily.  To get started, you will need a CSV file with the current filepath and filename in column A, and the new/desired filepath and filename in column B.  The CSV should NOT have a header row.')
print()
csv_input = input("Enter the filepath of the input CSV: ")

#check for header rows, return error to user if header rows detected
with open(csv_input, mode='r', newline='', encoding="utf8", errors='ignore') as f:
    lines = csv.reader(f)
    for line in lines:
        if os.path.isfile(line[0])==True:
            continue
        else:
            print()
            print('PROBLEM WITH SOURCE FILES! It looks like',line[0],'is not a valid file/location. Please delete any header rows and make sure all the source files are in the listed location and try again.')
            quit()
print()
print('This script will log its activities, including any naming issues or errors, in a new CSV.  You will need to provide a desired filepath and filename for this log.')
print()
csv_output = input("Enter the filepath/name for the log file:")
print()
print('Working...')
print()


#set up counters
filecount=0
errorcount=0
successcount=0
makepaths=list()
log={}

#open input CSV, go through each row of input
with open(csv_input, mode='r', newline='', encoding="utf8", errors='ignore') as userinput:
    for row in csv.reader(userinput):
        old_file=row[0]
        new_file=row[1]
        error_result=''
        success_result=''
        filecount=filecount+1

        if not os.path.isfile(new_file):  #validate new files 
            dupeissue=''
            extension=new_file[new_file.rfind("."):]
            if re.search(r'[.]\S\S\S$',extension):
                extissue=''
            else:
                errorcount=errorcount+1
                extissue='*improper extension format in new filename*'

            #check for spaces and nonprinting characters
            whitespacematches=re.findall(r'\s',new_file)
            if len(whitespacematches)>0:
                errorcount=errorcount+1
                whitespaceissue='*new filename/path contains spaces or nonprinting characters*'
            else:
                whitespaceissue=''

            #check for multiple periods
            periodmatches=re.findall(r'[.]',new_file)
            if len(periodmatches)>1:
                errorcount=errorcount+1
                periodissue='*filename/path contains multiple periods*'
            else:
                periodissue=''

            #check for invalid characters
            invalidcharmatches=re.findall(r'[^a-zA-Z0-9._\\\- ]',new_file)
            if len(invalidcharmatches)>0:
                errorcount=errorcount+1
                charissue='*filename/path contains special characters*'
            else:
                charissue=''
        else: #check for existing files
            errorcount=errorcount+1
            dupeissue='*file by that name already exists at the specifed location*'   
        
        #combine error messages into one string
        error_result=extissue+whitespaceissue+periodissue+charissue+dupeissue

        logentry={old_file:[new_file,error_result,success_result]}
        log.update(logentry)

for entry,changes in log.items():
    #for files with no issues, make list of directories to be created and source/destination pairs
    if changes[1]=='' and os.path.isdir(changes[0])==False:
        path=os.path.dirname(changes[0])
        makepaths.append(path)

#create the new directories needed
makepaths = list(dict.fromkeys(makepaths))
for path in makepaths:
    os.makedirs(path)

#rename and move files
for entry,changes in log.items():
    if changes[1]=='':
        try: #try renaming,log success
            os.rename(entry,changes[0])
            successcount += 1
            changes[2] = 'Success'
        except: #rename fails, log error
            errorcount += 1
            changes[1] = 'An unknown error has occurred'
    else:
        continue

#create output CSV, write header row
with open(csv_output, mode='a', newline='', encoding="utf8", errors='ignore') as outputlog:
    writer = csv.writer(outputlog, delimiter=',')
    writer.writerow(['Old File', 'New File', 'Error Result', 'Success Result'])

for entry,changes in log.items():
    itemlog=entry,changes[0], changes[1], changes[2]
    with open (csv_output, mode='a', newline='', encoding="utf8", errors='ignore') as outputlog:
        writer = csv.writer(outputlog)
        writer.writerow(itemlog)

#show results summary to user, point to output log for details
print('The process is completed.')
print('Files found: ',filecount)
print('Files renamed: ', successcount)
print('Issues identified: ', errorcount)
print('View the output log at: ',csv_output)