import operator
from urltools import ingestWord, extractUrlParts, tidyUrl
from csvtools import *
from settings import *


minUrlPartFrequency = 50

wordCounts = {}

# Load the header info
urlIdx = find_column_index_from_csv(headerCsvFilename, urlColumnName)

# Get the list of all CSV files
fileList = get_csv_filelist_from_folder(folder_with_csvs)

for filename in fileList:
    with open(filename) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if len(row) > 0:
                url = row[urlIdx]
                parts = extractUrlParts(tidyUrl(url))
                for part in parts:
                    ingestWord(wordCounts, part)


commonWords = sorted(wordCounts.items(), key=operator.itemgetter(1), reverse=True)
commonWords = [(urlpart,count) for urlpart, count in commonWords if count >= minUrlPartFrequency]

print('First 100')
for urlPart, count in commonWords[0:100]:
    print(urlPart, count)

print('------------------------------')
for urlPart, count in commonWords[100:]:
    print(urlPart, count)

#print(commonWords)
print('common url parts:')
print(len(list(commonWords)))


# Write out the list of common url parts
#save_simple_csv_list(commonUrlPartsFile, commonWords)
with open(url_part_filename, 'w', encoding='utf-8', newline='') as commonUrlPartsFile:
    writer = csv.writer(commonUrlPartsFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for urlPart, count in commonWords:
        writer.writerow([urlPart])



