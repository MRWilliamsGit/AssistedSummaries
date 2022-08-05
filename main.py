from scripts.API_caller import API_call
from scripts.clustering_class import ClusterClass
from scripts.summary_class import GenFinSummarizer

import streamlit as st
import json

# main function
# session state collects: gfs, r, term
def main():

    # Streamlit title
    st.title("Assisted Summaries")
    st.write(
        "This form uses clustering to assist in generating meaningful summaries of Twitter activity."
    )
    st.write("It bases its analysis on 50 relevant tweets pulled from Twitter's API.")

    term = st.text_input("Topic or search term:", " ")

    # collect Twitter data
    if "r" not in st.session_state or term != st.session_state.t:
        if term != " ":
            st.session_state.t = term
            # call API if it has not been collected before
            with st.spinner("Collecting Data"):
                r = API_call(term, 10)
                # with open('data2.json', 'w') as f:
                #    json.dump(r, f)

                # with open("data\data3.json", "r", encoding="utf8") as myfile:
                #   r = json.load(myfile)

                if r == "Oops":
                    st.error("Twitter data could not be loaded at this time")
                    st.stop()
                else:
                    st.session_state.r = r
                    st.experimental_rerun()

    # once data is collected, continue
    else:
        clusters = st.number_input(
            label="Number of perspectives:",
            min_value=2,
            max_value=5,
            value=2,
        )

        # cluster text
        with st.spinner("Clustering Tweets"):
            # initialize models
            if "gfs" not in st.session_state:
                st.session_state.gfs = GenFinSummarizer()
            cc = ClusterClass(clusters)

            # prep data and generate embeddings
            sumtext = st.session_state.gfs.Data_prep(st.session_state.r)
            clustext = cc.prep_text(sumtext)
            emb = cc.vectorize_text(clustext)

            # cluster text
            clusterdf = cc.k_cluster_text(sumtext, emb)

        # generate summaries for clusters
        with st.spinner("Generating Summaries"):
            for i in range(clusters):
                # get how many tweets in cluster, percentage, top words
                many = sum(clusterdf["cluster"] == i)
                perc = (many / len(clusterdf)) * 100
                wds = cc.imp_words(
                    emb,
                    clusterdf["cluster"] == i,
                    clusterdf[clusterdf["cluster"] == i]["text"],
                )
                # wds = ", ".join(cc.z_scores(emb, clusterdf["cluster"] == i))

                # prep data, calculate summary size, make summary
                text_list = st.session_state.gfs.make_cloud_chunks(
                    clusterdf[clusterdf["cluster"] == i]
                )
                sumlen = 200
                output = st.session_state.gfs.summarize(text_list, length=sumlen)

                # display
                st.write("Perspective #" + str(i + 1) + ":")
                st.caption("Percent of tweets: " + str(round(perc, 1)) + "%")
                st.caption("Most significant phrases/words: " + wds)
                st.write(output)


# Execute main function
if __name__ == "__main__":
    main()
