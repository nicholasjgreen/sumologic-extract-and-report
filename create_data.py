from urltools import *
from csvtools import *
from settings import *
import pickletools

# Load the header info
urlIdx = find_column_index_from_csv(headerCsvFilename, urlColumnName)
http_method_index = find_column_index_from_csv(headerCsvFilename, http_method_column_name)
orgId_index = find_column_index_from_csv(headerCsvFilename, orgIdColumnName)
appId_index = find_column_index_from_csv(headerCsvFilename, appIdColumnName)

# Get the list of all CSV files
fileList = get_csv_filelist_from_folder(folder_with_csvs)

# Load the list of url parts
url_parts = load_simple_csv_list(url_part_filename)
url_parts.append('')        # It's helpful to keep empty parts

# Load the feature list
features = pickletools.load(feature_list_filename)


# Create a template for feature counts
blank_feature_count_row = [0] * len(features)

# Accumulate feature counts here
feature_counts = {}

# Track if these features are used
feature_used = [False] * len(features)

def create_empty_feature_count():
    # Creates an array of zeroes, sized to the feature counts
    return blank_feature_count_row.copy()


def get_or_create_sample(appId, orgId):
    # Always returns an array that contains the feature count.
    # Will return either an existing one or an initialised/zeroed list
    key = '{}---{}'.format(appId, orgId)
    # Look it up
    if key in feature_counts:
        return feature_counts[key]
    # Create it
    f = create_empty_feature_count()
    # Store it
    feature_counts[key] = f
    # Return it
    return f


def map_url(raw_url, verb):
    parts = extractUrlParts(tidyUrl(raw_url))
    parts = list(map(lambda url_part: url_part if url_part in url_parts else uncommon_part_replacement, parts))
    return feature_name_from_method_and_url_parts(method, parts)


for filename in fileList:
    print("{} / {}".format(fileList.index(filename) + 1, len(fileList)))
    with open(filename) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if len(row) > 0:
                # Extract the data
                orgId = row[orgId_index]
                appId = row[appId_index]
                url = row[urlIdx]
                method = row[http_method_index]
                # Get the sample
                sample = get_or_create_sample(appId, orgId)
                # Calculate the feature index
                feature = map_url(url, method)
                if feature in features:
                    featureIdx = features.index(feature)
                    # Increase the count
                    sample[featureIdx] += 1
                    # Mark this feature as used
                    feature_used[featureIdx] = True


for idx in range(0, len(features)):
    if not feature_used[idx]:
        print("Unused features {} -- {}".format(idx, features[idx]))


#with open(data_filename, 'w', encoding='utf-8', newline='') as commonUrlPartsFile:
#    writer = csv.writer(commonUrlPartsFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for sample, counts in feature_counts.items():
#        counts.insert(0, sample)
#        writer.writerow(counts)


pickletools.save(data_filename, feature_counts)
