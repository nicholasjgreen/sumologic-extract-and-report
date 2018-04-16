import anony
import sys
import glob

inputFolder = sys.argv[1]
outputFolder = sys.argv[2]

fileList = glob.glob(inputFolder + r'\*.csv')
#print(fileList)

anony.smashCsvFile(fileList[0], 'test.csv', [0,1], [2,3,4])

#for filename in fileList:
#    smashCsvFile(filename)