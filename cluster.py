from settings import *
from sklearn.cluster import KMeans
import pickletools
import csvtools


def matching_labels(lst, val):
    return [i for i,x in enumerate(lst) if x == val]


def get_interesting_centroid_features(centroids, feature_names):
    # Returns a list where each row has a list of "interesting" features for the centroid
    # NB: Interesting generally means a high or low value compared to the average
    lst = []
    for centroid in centroids:
        lst.append(['{}({})'.format(feature_names[idx], c) for idx,c in enumerate(centroid) if not (-0.05 < c < 1.0)])
    return lst


def do_cluster():
    label_names = pickletools.load(labels_filename)
    X_scaled = pickletools.load(normalized_data_filename)
    
    cluster_count = 10
    
    print('Clustering...')
    kmeans = KMeans(n_clusters=cluster_count, max_iter=1000, n_jobs=4, tol=0.0001).fit(X_scaled)
    
    create_lists(cluster_count, kmeans, label_names)

    features = save_centroids(kmeans)

    find_interesting_features(cluster_count, features, kmeans)


def find_interesting_features(cluster_count, features, kmeans):
    # Let's pull out the interesting features for each centroid
    centroids = kmeans.cluster_centers_.tolist()
    interesting_features = get_interesting_centroid_features(centroids, features)
    for centroidIdx in range(cluster_count):
        these_interesting_features = interesting_features[centroidIdx]
        #print('{} has {} interesting features'.format(centroidIdx, len(these_interesting_features)))
        csvtools.save_simple_csv_list(centroid_interesting_features_filename_format.format(centroidIdx),
                                      these_interesting_features)


def save_centroids(kmeans):
    print('Saving the centroids')
    features = pickletools.load(reduced_feature_filename)
    centroids = kmeans.cluster_centers_.tolist()
    centroids.insert(0, features)
    csvtools.save_csv_lines(centroids_filename, centroids)
    return features


def extract_appid_from_label(label):
    # Gets the appid from the label we have used for the data
    return label[0:36]


def create_lists(cluster_count, kmeans, label_names):
    print('Creating lists...')
    for centroidIdx in range(cluster_count):
        connectionIdxs = matching_labels(kmeans.labels_, centroidIdx)
        these_label_names = [label_names[i] for i in connectionIdxs]
        these_appids = sorted(list(set([extract_appid_from_label(label) for label in these_label_names])))
        csvtools.save_simple_csv_list(centroid_filename_format.format(centroidIdx), these_label_names)
        print('Centroid {} has a population of {}, and {} apps'.format(centroidIdx, len(connectionIdxs),
                                                                       len(these_appids)))


if __name__ == '__main__':
    do_cluster()
