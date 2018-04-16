# Submits search job, waits for completion, then prints and emails results.
# Pass the query via stdin.
#
# cat query.sumoql | python search-job.py <accessId> <accessKey> \
# <endpoint> <fromDate> <toDate> <timeZone>
#
# Note: fromDate and toDate must be either ISO 8601 date-times or epoch
#       milliseconds
#
# Example:
#
# cat query.sumoql | python search-job.py <accessId> <accessKey> \
# https://api.us2.sumologic.com/api/v1/ 1408643380441 1408649380441 PST

import sys
import os
import time
import logging
import requests
import math
import csv
import os
import sumologic.sumologic

sumoUrl = 'https://api.us2.sumologic.com/api/v1/'
timeZone = 'NZ'
accessId = os.environ['SUMO_ACCESS_ID']
accessKey = os.environ['SUMO_ACCESS_KEY']


logging.basicConfig(level=logging.ERROR)

#from sumologic import SumoLogic


LIMIT = 10000

sumo = sumologic.sumologic.SumoLogic(accessId, accessKey, sumoUrl)
#args = sys.argv
#sumo = sumologic.sumologic.SumoLogic(args[1], args[2], args[3])
#fromTime = args[4]
#toTime = args[5]
#timeZone = args[6]


# Which hour? -- from command line
hoursAgo = int(sys.argv[1])
minutesOld = hoursAgo * 60
minutesOfQuery = 60

now = math.floor(time.time() * 1000) - (minutesOld * 60 * 1000)
toTime = str(now)
fromTime = str(now - (minutesOfQuery * 60 * 1000))

delay = 5
q = '_sourceCategory=prod/app/nlog/log cat2=site_api_global | where !isnull(api_baseurl)| fields api_baseurl, api_providerid, api_orgid, api_httpmethod, api_duration'
fieldNames = ['api_providerid', 'api_orgid', 'api_baseurl', 'api_httpmethod', 'api_duration']

folderName = 'data_{}'.format(now)
if not os.path.exists(folderName):
    os.makedirs(folderName)

try:
    sj = sumo.search_job(q, fromTime, toTime, timeZone)
except requests.exceptions.HTTPError as err:
    print(err.response)
    print(err.errno)
    print(err)
    if err.errno == 400:
        print(err.response)
    else:
        raise

print('Job started')
status = sumo.search_job_status(sj)
while status['state'] != 'DONE GATHERING RESULTS':
    print('waiting for results...')
    if status['state'] == 'CANCELLED':
        print('Cancelled!')
        break
    time.sleep(delay)
    status = sumo.search_job_status(sj)


#print(status)
print(status['state'])


if status['state'] == 'DONE GATHERING RESULTS':
    count = status['recordCount']
    useMessages = False

    # If there are no records, then look for messages
    if count == 0:
        count = status['messageCount']
        useMessages = True
    print('Result count = ' + str(count))

    limit = count if count < LIMIT and count != 0 else LIMIT # compensate bad limit check
    offset = 0
    fileNumber = 0
    while(offset < count):
        # Progress update
        print('------[ {}% Fetching from {} of {} ]------'.format(offset*100//count, offset, count))

        # This isn't pretty, but I don't know a better way to switch between methods
        if useMessages:
            r = sumo.search_job_messages(sj, limit=limit, offset=offset)
            theList = r['messages']
        else:
            r = sumo.search_job_records(sj, limit=limit, offset=offset)
            theList = r['records']

        # Get the field names
        if len(fieldNames) == 0:
            fieldNames = list(f['name'] for f in r['fields'])

        # Write to file
        fileNumber = fileNumber + 1
        with open(r'%s\%05d.csv' % (folderName, fileNumber), 'w', encoding='utf-8', newline='') as theTotalsFile:
            writer = csv.writer(theTotalsFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # Process these records
            for rec in theList:
                thisRow = list(rec['map'][fieldName] for fieldName in fieldNames)
                writer.writerow(thisRow)

        # Move along to the next set of records
        offset += len(theList)

