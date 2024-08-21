#set up RSS feed parsing
import feedparser
url=input('enter RSS URL:')
feed=feedparser.parse(url)

#set up CSV file and header row
import csv
with open('rss_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['dc.title', 'dc.date.issued', 'dc.description.abstract', 'dc.description', 'filename-audio', 'filename-image','dc.type.','dc.contributor.author','id','collection'])

#validating each entry in RSS and converting into variables
for entry in feed.entries:
    try:
        title=entry.title
    except:
        title="No Title Available"
    try:
        date=entry.published
    except:
        date="No Date Available"
    try:
        abstract=entry.description
    except:
        abstract="No Abstract Available"
    try:
        description=entry.itunes_duration
    except:
        description="No Runtime Available"
    try:
        files=entry.enclosures
    except:
        files="No Files Available"
    try:
        image=entry.image,"AND/OR",entry.itunes_image
    except:
        image="No Image Available"
    type="Audio"
    
#write entry metadata into a new row
    entrydata=[title, date, abstract, description, files, image, type]
    with open('rss_data.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(entrydata)