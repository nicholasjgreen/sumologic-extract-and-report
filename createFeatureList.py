from urltools import *
from csvtools import *
import pickletools
from settings import *

# some settings

# Get the list of all CSV files
fileList = get_csv_filelist_from_folder(folder_with_csvs)

# Load the header info
urlIdx = find_column_index_from_csv(headerCsvFilename, urlColumnName)
http_method_index = find_column_index_from_csv(headerCsvFilename, http_method_column_name)

# Get the list of all CSV files
fileList = get_csv_filelist_from_folder(folder_with_csvs)

# Load the list of url parts
url_parts = load_simple_csv_list(url_part_filename)
url_parts.append('')        # It's helpful to keep empty parts

# collect all the urls into this list
features = {}

for filename in fileList:
    with open(filename) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if len(row) > 0:
                url = row[urlIdx]
                method = row[http_method_index]
                parts = extractUrlParts(tidyUrl(url))
                # Map the parts so that we change parts that are uncommon into the uncommon_part_replacement
                parts = list(map(lambda url_part: url_part if url_part in url_parts else uncommon_part_replacement, parts))
                mapped_url = feature_name_from_method_and_url_parts(method, parts)
                if mapped_url not in features and is_valid_http_method(method):
                    features[mapped_url] = mapped_url
                    print(mapped_url)

features = list(sorted(list(features)))

# Report
for feature in features:
    print(feature)

pickletools.save(feature_list_filename, features)
save_simple_csv_list(feature_list_csv_filename, features)