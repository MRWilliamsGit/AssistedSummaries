#https://towardsdatascience.com/how-to-easily-cluster-textual-data-in-python-ab27040b07d8
from sklearn.feature_extraction.text import TfidfVectorizer
#import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

class ClusterClass():
    def __init__(self):
    
        print("Initializing Clustering Object...")
        self.vectorizer = TfidfVectorizer(stop_words={'english'})

    #params: list of texts to cluster
    #returns: list of embeddings
    def vectorize(self, text):
        #generate embeddings for text based on TF-IDF
        X = self.vectorizer.fit_transform(text)
        return X

    #params: list of texts to cluster
    #returns: 
    def cluster_text(self, text, X):

        #find optimal k (can be done automatically?)
        # Sum_of_squared_distances = []
        # K = range(2,10)
        # for k in K:
        #    km = KMeans(n_clusters=k, max_iter=200, n_init=10)
        #    km = km.fit(X)
        #    Sum_of_squared_distances.append(km.inertia_)
        # plt.plot(K, Sum_of_squared_distances, 'bx-')
        # plt.xlabel('k')
        # plt.ylabel('Sum_of_squared_distances')
        # plt.title('Elbow Method For Optimal k')
        # plt.show()

        # print('How many clusters do you want to use?')
        # true_k = int(input())
        true_k = 2

        #cluster the embeddings using k-means
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
        model.fit(X)

        labels=model.labels_
        clusters=pd.DataFrame(list(zip(text,labels)),columns=['title','cluster'])
        #print(clusters.sort_values(by=['cluster']))

        for i in range(true_k):
            print(clusters[clusters['cluster'] == i])
            
        return