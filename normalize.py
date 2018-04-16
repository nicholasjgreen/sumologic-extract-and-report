from settings import *
import pickletools
import numpy as np

# Load the data file
#X_dict = pickletools.load(data_filename)
X = pickletools.load(reduced_data_filename)

# Remove the labels
#print('Getting labels and values')
#labels = list(X_dict.keys())
#X = np.array(list(X_dict.values()))


# Scale it
print('Scaling...')
#X_scaled = preprocessing.scale(X)
X_scaled = np.log(X + 1)

#pickletools.save(labels_filename, labels)
pickletools.save(normalized_data_filename, X_scaled)


