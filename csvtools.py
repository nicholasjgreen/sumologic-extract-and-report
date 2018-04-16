import glob
import csv
from math import inf

def get_csv_filelist_from_folder(folderName):
    return glob.glob(folderName + r'\*\*.csv')



def find_column_index_from_csv(filename, column_name):
    with open(filename) as csvFile:
        reader = csv.reader(csvFile)
        header = next(reader)
        return header.index(column_name)


def load_simple_csv_list(filename):
    with open(filename) as csvFile:
        reader = csv.reader(csvFile)
        item_list = []
        for row in reader:
            if len(row) > 0:
                item_list.append(row[0])
    return item_list


def load_csv_lines(filename, max_lines=inf):
    with open(filename) as csvFile:
        reader = csv.reader(csvFile)
        item_list = []
        line_num = 0
        for row in reader:
            line_num += 1
            if len(row) > 0:
                item_list.append(row)
            if line_num >= max_lines:
                break
        return item_list


def save_simple_csv_list(filename, items):
    print('Saving simple csv list ' + filename)
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in items:
            writer.writerow([item])


def save_csv_lines(filename, lines):
    print('Saving csv lines ' + filename)
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in lines:
            writer.writerow(line)