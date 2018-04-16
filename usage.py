import csv
import re
import operator

wordCounts = {}

exprGuid = re.compile(r'(\{){0,1}[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}(\}){0,1}')
exprFile = re.compile(r'\/[0-9a-zA-Z%!@#$^&*\-_()<>.]*.(pdf|jpg|jpeg|png|tif|bmp|csv|msg|xlsx|xls|docx|doc)$')

def tidyUrl(url):
    url = url.lower()
    url = exprGuid.sub('<SOME_GUID>', url)
    url = exprFile.sub('/<FILE>', url)
    return url


def extractUrlParts(url):
    return url.split('/')


def ingestWord(word):
    # Skip empty
    if word == '':
        return

    # Add or increase
    if not word in wordCounts:
        wordCounts[word] = 1
    else:
        wordCounts[word]  = wordCounts[word] + 1


inputFilename = r'C:\Users\nick.green\Downloads\slowqueries_search-results-2017-08-31T16-42-49.283-0700.csv'
with open(inputFilename) as csvFile:
    reader = csv.reader(csvFile)
    header = next(reader)
    urlIdx = header.index("api_baseurl")
    for row in reader:
        url = row[urlIdx]
        parts = extractUrlParts(tidyUrl(url))
        for part in parts:
            ingestWord(part)


commonWords = sorted(wordCounts.items(), key=operator.itemgetter(1),reverse=True)

print(commonWords)
print(len(list(commonWords)))
