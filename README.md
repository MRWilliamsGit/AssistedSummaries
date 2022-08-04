# AssistedSummaries
Social Media has become the most prominent source of information for most modern people, but individual posts do not tell the whole story, and collections of posts are difficult to summarize due to their numbers and diversity. 

In order to help generate meaningful summaries, this project uses clustering to first sort tweets into sets by topic, then generates individual summaries for each cluster. The most important keywords and relative saturation of each cluster are provided as additional insight.

## Data
This project uses the Twitter API to collect sets of 20 tweets related to the search term provided by the user. Tweets are cleaned and pre-processed by removing links, @Usernames and special characters. For clustering purposes, words are further reduced by removing stop-words and lemmatizing.

## Clustering
The tweets are translated into vectors using TF_IDF, which measures the importance of each word in the tweet relative to its importance overall. The tweets are then sorted based on simple K-Means clustering. 

## Summarization
Once the tweets have been sorted, they are summarized by a pre-trained [DistilBART model](https://huggingface.co/sshleifer/distilbart-cnn-12-6). BART uses bi-directional encoding like BERT, but causal decoding like GPT​, and generally outperforms BERT in summarization tasks.

## Explainability
The words that contribute most to each cluster are determined through their z-scores, which measure how important they are to the cluster relative to how important they are on average. The top three words that are more important to the cluster than they are to other clusters, are displayed.

## Deployment
Please enjoy interacting with this tool through its public app: https://mrwilliamsgit-assistedsummaries-main-3agmtw.streamlitapp.com/

## Local Deployment
1. Obtain a Twitter Developer login and app bearer token. [Instructions Here](https://developer.twitter.com/en/support/twitter-api/developer-account)
2. Clone this repository to your local environment and add an additional folder named '.streamlit' (note the period).
3. In this folder, add a .toml file named 'secrets.toml' with your Twitter bearer token as content in this format: 'BearerToken = 'AAAAAAAAAAA''.
5. Now that you have all the information you need, install the dependancies to your local environment.
```
pip install -r requirements.txt
```
6. To run the app locally, use the command line terminal.
```
streamlit run main.py
```
