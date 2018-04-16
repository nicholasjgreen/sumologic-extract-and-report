from settings import *
import pickletools
import numpy as np


# Settings
feature_min_connection_count = 1
feature_min_app_count = 1


# Load data
features = pickletools.load(feature_list_filename)
X_dict = pickletools.load(data_filename)

# Remove the labels
print('Getting labels and values')
labels = list(X_dict.keys())
X = np.array(list(X_dict.values()))

useful_features = []

for f in range(0, len(features)):
    counts_for_this_feature = X[:, f]
    connection_idxs = list(x for x in counts_for_this_feature if x > 0)
    connection_count = len(connection_idxs)
    appIds = list(set(list(labels[connection_idx][0:36] for connection_idx in connection_idxs)))
    app_count = len(appIds)
    call_count = sum(counts_for_this_feature)
    
    #print('{}/{}/{} - {}'.format(connection_count, app_count, call_count, features[f]))
    if connection_count >= feature_min_connection_count and app_count > feature_min_app_count:
        useful_features.append(features[f])

pickletools.save(reduced_feature_filename, useful_features)
print('Saved the {} best features'.format(len(useful_features)))


# Work out idxs of which ones stay
feature_idxs_to_keep = [features.index(feature) for feature in useful_features]

# Build a new X from the bits we want to keep
X_reduced = []
for x in X:
    X_reduced.append([x[idx] for idx in feature_idxs_to_keep])

X_red = np.array(X_reduced)

# Save it
pickletools.save(reduced_data_filename, X_red)
