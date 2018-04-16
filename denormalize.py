from settings import *
import numpy as np
from csvtools import *

# Load the centroids
centroids_data = load_csv_lines(centroids_filename)

# Extract labels and data
labels = centroids_data[0]
centroids = np.array(centroids_data[1:]).astype(np.float)

# Denormalize
# 1. Convert back from log
# 2. Subtract 1
# 3. Convert to absolute int
denormalized = np.abs(np.round(np.exp(centroids) - 1).astype(np.int))

# Convert back to a list with headers
centroid_list = denormalized.tolist()
centroid_list.insert(0, labels)

# Save
save_csv_lines(denormalized_centroids_filename, centroid_list)