#!/usr/bin/env python3

"""
This is a script that takes a NARA Preservation Action Plan CSV file (from https://github.com/usnationalarchives/digital-preservation/tree/master/Digital_Preservation_Plan_Spreadsheet) and transforms each line into a formatted markdown file. 
See example output markdown file here: https://gist.github.com/hannahlwang/03e9f5327e2e81ff18eaa936bb2f4fa0
"""

# Import pandas to process CSV file
import pandas as pd

# Read the Preservation Action Plan CSV file to a pandas DataFrame. 
print('What is the file path for the Preservation Action Plan CSV?')
csvin = input()
df = pd.read_csv(csvin)

# Clean up the DataFrame by removing blank rows and replacing NaN values with empty strings
dfClean = df[df['Format Name'].notna()].fillna('')

# Turn the DataFrame into a list of dictionaries, with one dictionary per file format record
formatDictList = dfClean.to_dict('records')

for formatDict in formatDictList:

  # Create a markdown file for each file format, with the naming convention NF#####.md
  filename = str(formatDict['NARA Format ID'] + '.md')
  f = open(filename, 'w')

  # Each markdown file has the same heading, and a table that starts with the same header row
  f.write('''# File Format Preservation Plan
| Field | Value |
| ----------- | ----------- |
''')

  for field in formatDict:
    value = formatDict[field]

    # Replace pipes inside values with semicolons
    if type(value) == str:
      value = value.replace('|', '; ')

    # Format any URLs so that they are hyperlinked in markdown
    if value.startswith('http'):
      value = '<%s>' % value

    # Write each field-value pair into a row in the markdown table
    f.write('| %s | %s | \n' % (field, value))
