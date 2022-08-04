from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import contractions
import nltk
from nltk.stem import WordNetLemmatizer

import pandas as pd
import numpy as np
import regex as re
import csv

# class for text clustering
# params: number of clusters
class ClusterClass:
    def __init__(self, ksize):

        print("Initializing Clustering Objects...")
        self.ksize = ksize
        self.vectorizer = TfidfVectorizer(stop_words={"english"}, ngram_range=(1,2))
        self.lemmatizer = WordNetLemmatizer()
        self.model = KMeans(
            n_clusters=self.ksize, init="k-means++", max_iter=200, n_init=10
        )

        #downloads
        #nltk.download("stopwords")
        nltk.download("wordnet")
        nltk.download("omw-1.4")


    # params: list of texts to cluster
    # returns: text prepped for embeddings
    def prep_text(self, text):

        newtext = []

        for t in text:
            # Note: TfidfVectorizer will handle stopwords
            # remove numbers, contractions, punctuation
            t = t.lower()
            t = re.sub(r'\d+' , '', t)
            t = contractions.fix(t)
            punct = '''!()[]{};«№»:'",`./?@=#$-(%^)+&[*_]~'''
            for p in punct:
                t = t.replace(p, "")
            
            # lemmatize
            words = t.split()
            lemwords = [self.lemmatizer.lemmatize(word, "v") for word in words]
            t = ' '.join(lemwords)
            newtext.append(t)
        
        return newtext

    # params: list of texts to cluster
    # returns: list of embeddings for text based on TF-IDF
    def vectorize_text(self, text):
        #this will already lowercase, remove stopwords, etc
        X = self.vectorizer.fit_transform(text)
        return X

    # params: list of texts to cluster, embeddings for each text
    # returns: dataframe with text + which cluster it belongs to (k-means)
    def k_cluster_text(self, text, X):

        # cluster the text
        self.model.fit(X)

        # create dataframe with text and associated cluster label
        labels = self.model.labels_
        cluster_df = pd.DataFrame(list(zip(text, labels)), columns=["text", "cluster"])

        # return dataframe
        # cluster_df.to_csv("data3_1", sep='\t', encoding='utf-8')
        return cluster_df
    
    # params: embeddings already created by "vectorize_text"
    # params: bool list of what text belong to the cluster
    # returns: top three words with highest z-scores for this cluster
    # z-score = (IDF average of word in cluster - IDF average of word in corpus)
    # /(standard deviation of IDF score)
    def z_scores(self, emb, w):
        # get a numpy matrix of IDF scores (a row for each textblock, column for each word)
        tfidf = emb.todense()

        # get average IDF score for each word: entire corpus
        cormean = np.mean(tfidf, axis=0)

        # get average IDF score for each word: just this cluster
        cludata = tfidf[w, :]
        clumean = np.mean(cludata, axis=0)

        # get standard deviation for each word
        dev = np.std(tfidf, axis=0)

        # calculate z-score for each word 
        diff = clumean-cormean 
        score = diff / dev
        score = score.tolist()

        # get the word list
        wds = self.vectorizer.vocabulary_.items()

        # get the top words
        z_words = []
        zwds = sorted(zip(score[0], wds), reverse=True)
        for z in zwds[:5]:
            z_words.append(z[1][0])

        return z_words