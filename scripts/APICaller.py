import requests
import streamlit as st
import json

#define search twitter function - returns 10 tweets
#https://towardsdatascience.com/searching-for-tweets-with-python-f659144b225f
def search_twitter(query):

    bearer_token = st.secrets['BearerToken']
    tweet_fields = "tweet.fields=text"

    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
