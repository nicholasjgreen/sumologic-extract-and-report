import base64
import hashlib
import csv

def smashStrings(strings):
    m = hashlib.md5()
    for str in strings:
        m.update(str.encode('utf-8'))
    return base64.b64encode(m.digest()).decode('utf-8')


def smashCsvFile(inputFilename, outputFilename, columnsToSmash, columnsToKeep):
    with open(inputFilename) as inCsvFile:
        with open(outputFilename, 'w', encoding='utf-8', newline='') as outCsvFile:
            reader = csv.reader(inCsvFile)
            writer = csv.writer(outCsvFile)
            for inRow in reader:
                #print(inRow)
                #print(columnsToSmash)
                if(len(inRow) > 0):
                    smashedData = smashStrings([inRow[i] for i in columnsToSmash])
                    writeData = [inRow[i] for i in columnsToKeep]
                    writeData.insert(0, smashedData)
                    writer.writerow(writeData)
