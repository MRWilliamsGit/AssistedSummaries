from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans

import contractions
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

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
        self.vectorizer = TfidfVectorizer(stop_words={"english"}, ngram_range=(1, 2))
        self.lemmatizer = WordNetLemmatizer()
        self.model = KMeans(
            n_clusters=self.ksize, init="k-means++", max_iter=200, n_init=10
        )

        # downloads
        # nltk.download("stopwords")
        nltk.download("wordnet")
        nltk.download("omw-1.4")

    # params: list of texts to cluster
    # returns: text prepped for embeddings
    def prep_text(self, text):

        newtext = []

        for t in text:
            # remove numbers, contractions, punctuation
            t = t.lower()
            t = re.sub(r"\d+", "", t)
            t = contractions.fix(t)
            punct = """!()[]{};«№»:'",`./?@=#$-(%^)+&[*_]~"""
            for p in punct:
                t = t.replace(p, "")

            words = t.split()

            # remove stopwords
            # Note: TfidfVectorizer is supposed to handle stopwords, but it doesn't seem to
            swds = set(stopwords.words("english"))
            ft = []
            for w in words:
                if w not in swds:
                    ft.append(w)
            words = ft

            # lemmatize
            lemwords = [self.lemmatizer.lemmatize(word, "v") for word in words]
            t = " ".join(lemwords)
            newtext.append(t)

        return newtext

    # params: list of texts to cluster
    # returns: list of embeddings for text based on TF-IDF
    def vectorize_text(self, text):
        # this will already lowercase, remove stopwords, etc
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
    # returns: top five words/phrases with highest z-scores for this cluster
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
        diff = clumean - cormean
        score = diff / dev
        score = score.tolist()

        # get the word list
        wds = self.vectorizer.vocabulary_.items()

        # get the top words
        zwds = sorted(zip(score[0], wds), reverse=True)
        # z_words = []
        # for z in zwds[:5]:
        #    z_words.append(z[1][0])

        return zwds

    # params: list of tweets in the cluster
    # returns: word/phrase count for the cluster
    def wd_count(self, text):

        # prep (lemmatize, etc)
        text = self.prep_text(text)

        # transform all tweets to list of words
        blocklist = [" ".join(text)]

        # get wordcount
        cv = CountVectorizer(ngram_range=(1, 2))
        cv_fit = cv.fit_transform(blocklist)
        word_list = cv.get_feature_names_out()

        # zip words/phrases and their counts
        count_list = np.asarray(cv_fit.sum(axis=0))[0]
        cwds = sorted(zip(count_list, word_list), reverse=True)

        return cwds

    # params: embeddings already created by "vectorize_text"
    # params: bool list of what tweets belong to the cluster
    # params: list of tweets in the cluster
    # returns: top distinguishing words for the cluster
    # uses: z_scores and wd_count internally
    def imp_words(self, emb, w, text):
        # get list of z-scores and word counts
        zwds = self.z_scores(emb, w)
        cwds = self.wd_count(text)

        # combine
        cwds_df = pd.DataFrame(cwds, columns=["count", "phrase"])
        zwds_df = pd.DataFrame(zwds, columns=["zscore", "tuple"])
        tuple_df = pd.DataFrame(zwds_df["tuple"].tolist(), columns=["phrase", "ID"])
        tuple_df["zscore"] = zwds_df["zscore"]
        all_df = tuple_df.merge(cwds_df, how="right", on="phrase")
        # print(all_df)

        # remove count 1, negative z-score
        df = all_df.drop(all_df[(all_df["count"] == 1)].index)
        df = df.drop(df[(df["zscore"] < 0.5)].index)

        # multiply zscore and count to find significance
        # z-score should have more importance since it already considers count
        df["impscore"] = (10 * df["zscore"]) * (df["count"] / 2)

        df = df.sort_values(by=["impscore"], ascending=False)
        # print(df)

        # return information
        # catch for no returns
        if len(df) > 5:
            hi = df["phrase"].tolist()
            hi = hi[:5]
            return ", ".join(hi)
        elif len(df) == 0:
            return "(there are no significant phrases for this cluster)"
        else:
            hi = df["phrase"].tolist()
            return ", ".join(hi)
