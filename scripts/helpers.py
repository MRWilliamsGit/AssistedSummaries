import requests
import streamlit as st

# params: search term and number of results to get (10-100)
# returns: response from Twitter API
def API_call(query, n):

    # get call params
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": "Bearer {}".format(st.secrets["BearerToken"])}
    query_params = {"query": query + " -is:retweet", "max_results": n}

    # call API
    res = requests.request("GET", url, headers=headers, params=query_params)

    # if call is good, return json response
    if res.status_code != 200:
        #raise Exception(res.status_code, res.text)
        return "Oops"
    else:
        return res.json()
