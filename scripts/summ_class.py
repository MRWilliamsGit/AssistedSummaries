import re
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Create class for generative summarization
class GenFinSummarizer:
    def __init__(self):

        print("Initializing Object...")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "sshleifer/distilbart-cnn-12-6"
        )
        self.tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

    # param: list of text chunks to summarize (may be only one item but must be list)
    # param: length of summary to provide for each chunk
    # returns: summary generated by generative summary model
    def summarize(self, text, length):

        print("Generating Summary...")
        summary = ""
        for t in text:
            input_ids = self.tokenizer.encode(
                t, return_tensors="pt", max_length=1024, truncation=True
            )
            output = self.model.generate(
                input_ids,
                max_length=length,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
            )
            output = self.tokenizer.decode(output[0])
            summary = summary + " " + output

        summary = summary.split("</s>")[-2].split("<s>")[-1].strip()
        return summary

    # params: df of post info returned from API
    # returns: list of text blocks of titles and text, used for GenFinSummarizer
    def make_cloud_chunks(self, tw_df):

        chunk_size = 1024
        textblock = []

        # go post by post and add together in chunks that are less than 1024 words
        for tweet in tw_df["content"]:
            # if it's too long, chunk it
            # tweets will of course not be this long; this is left for other deployemnts
            if len(tweet.split(" ")) > chunk_size:
                wds = tweet.split(" ")
                nchunks = int(len(wds) / chunk_size) + (len(wds) % chunk_size > 0)
                lchunks = int(len(wds) / nchunks) + (len(wds) % nchunks > 0)
                chunked = [wds[i : i + lchunks] for i in range(0, len(wds), lchunks)]
                for c in range(len(chunked)):
                    chunked[c] = " ".join(chunked[c])
            else:
                chunked = [tweet]

            # add the chunk(s) to textblock
            for c in chunked:
                if len(textblock) == 0:
                    textblock.append(c)
                else:
                    chunkq = textblock[len(textblock) - 1] + " " + c
                    if len(chunkq.split()) < chunk_size:
                        textblock[len(textblock) - 1] = chunkq
                    else:
                        textblock.append(c)

        # print(textblock)
        return textblock

    # params: json response from Twitter API
    # returns: list of cleaned post text, and dataframe version for future development
    def Data_prep(self, r):

        # list for posts
        tlist = []
        # dataframe for posts
        posts_df = pd.DataFrame()

        # get cleaned data
        for post in r["data"]:

            # clean out special characters, links, @, etc.
            this = post["text"]
            this = this.replace("\n", " ")
            this = re.sub(r"http\S+", "", this)
            this = re.sub(r"@\S+", "", this)
            gone = "[]//$\\()"
            for g in gone:
                this = this.replace(g, "")
            this = this.strip()

            # append to list
            tlist.append(this)

            # append to dataframe
            posts_df = pd.concat(
                [posts_df, pd.DataFrame({"content": this}, index=[len(posts_df) + 1])]
            )

        return tlist, posts_df
