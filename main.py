from scripts.helpers import API_call
from scripts.clustering_class import ClusterClass
from scripts.summary_class import GenFinSummarizer
import streamlit as st
import json

# main function
# session state collects: gfs, cc, r, term
def main():

    # Streamlit title
    st.title("Assisted Summaries")
    st.write(
        "This form uses clustering to assist in generating meaningful summaries of twitter topics."
    )

    term = st.text_input("Enter a topic or search term:", " ")

    # collect Twitter data
    if "r" not in st.session_state or term != st.session_state.t:
        if term != " ":
            st.session_state.t = term
            # call API if it has not been collected before
            with st.spinner("Collectiong Data"):
                # first collect info from API
                r = API_call(term, 10)
                # with open('data3.json', 'w') as f:
                #    json.dump(r, f)

                # with open("data\data2.json", "r", encoding="utf8") as myfile:
                #    r = json.load(myfile)

                # if info is not collected, stop there, otherwise save to session state
                if r == "Oops":
                    st.error("Twitter data could not be loaded at this time")
                    st.stop()
                else:
                    st.session_state.r = r
                    st.experimental_rerun()

    # once data is collected, continue
    else:
        clusters = st.number_input(
            label="Enter the number of perspectives to find:",
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
            work = st.session_state.gfs.Data_prep(st.session_state.r)
            emb = cc.vectorize_text(work)

            # cluster text
            clusterdf = cc.k_cluster_text(work, emb)

        # generate summaries for clusters
        with st.spinner("Generating Summaries"):
            for i in range(clusters):
                text_list = st.session_state.gfs.make_cloud_chunks(
                    clusterdf[clusterdf["cluster"] == i]
                )
                output = st.session_state.gfs.summarize(text_list, length=200)
                st.write("Perspective #" + str(i + 1) + ":")
                st.write(output)


# Execute main function
if __name__ == "__main__":
    main()
