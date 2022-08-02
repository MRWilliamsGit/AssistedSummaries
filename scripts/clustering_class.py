#https://towardsdatascience.com/how-to-easily-cluster-textual-data-in-python-ab27040b07d8
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

class ClusterClass():
    def __init__(self, ksize):
    
        print("Initializing Clustering Objects...")
        self.ksize = ksize
        self.vectorizer = TfidfVectorizer(stop_words={'english'})
        self.model = KMeans(n_clusters=self.ksize, init='k-means++', max_iter=200, n_init=10)

    #params: list of texts to cluster
    #returns: list of embeddings
    def vectorize_text(self, text):
        #generate embeddings for text based on TF-IDF
        X = self.vectorizer.fit_transform(text)
        return X

    #params: list of texts to cluster
    #returns: dataframe with text + which cluster it belongs to
    def cluster_text(self, text, X):

        #cluster the text
        self.model.fit(X)

        #create dataframe with text and associated cluster label
        labels=self.model.labels_
        cluster_df=pd.DataFrame(list(zip(text,labels)),columns=['text','cluster'])
            
        #return dataframe
        return cluster_df