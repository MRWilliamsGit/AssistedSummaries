import pandas as pd
import requests
import re
import streamlit as st
import json

#params: search term and number of results to get (10-100)
#returns: response from Twitter API
def API_call(query,n):

    #get call params
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": "Bearer {}".format(st.secrets['BearerToken'])}
    query_params = {'query': query+' -is:retweet', 'max_results': n}

    #call API
    res = requests.request("GET", url, headers=headers, params=query_params)

    #if call is good, return json response
    if res.status_code != 200:
        raise Exception(res.status_code, res.text)
    else:
        return res.json()

#params: json response from Twitter API
#returns: list of cleaned post text, and dataframe version for future development
def Data_prep(r):
    
    #list for posts
    tlist = []
    #dataframe for posts
    posts_df = pd.DataFrame()

    #get cleaned data
    for post in r['data']:

        #clean out special characters, links, @, etc.
        this = post['text']
        this = this.replace("\n", ' ')
        this = re.sub(r'http\S+', '', this)
        this = re.sub(r'@\S+', '', this)
        gone = '[]//$\\()'
        for g in gone:
            this = this.replace(g, '')
        this = this.strip()

        #append to list
        tlist.append(this)

        #append to dataframe
        posts_df = pd.concat([posts_df, pd.DataFrame({
            'content': this
        }, index=[len(posts_df)+1])])

    return tlist, posts_df