from scripts.APICaller import search_twitter

def main():
    term = "abortion"

    work = search_twitter(term)
    #work = connect_to_endpoint()
    print(work)

    #tweets = get_tweets(term)
    #tweets = convert_to_df(tweets)

# Execute main function
if __name__ == "__main__":
    main()