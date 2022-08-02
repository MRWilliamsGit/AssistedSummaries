# AssistedSummaries
This project uses clustering to assist in generating meaningful summaries of Twitter topics.

## Data
This project uses the Twitter API to collect sets of tweets related to the search term provided by the user.

## Clustering
The tweets are translated into vectors using TF_IDF, and then sorted based on simple K-Means clustering.

## Summarization
Once the tweets have been sorted, they are summarized by a pre-trained DistillBART model.

## Deployment
Please enjoy interacting with this tool through its public app: https://mrwilliamsgit-assistedsummaries-main-3agmtw.streamlitapp.com/
