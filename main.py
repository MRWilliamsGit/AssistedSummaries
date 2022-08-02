from scripts.helpers import API_call
from scripts.clustering_class import ClusterClass
from scripts.summary_class import GenFinSummarizer
import json
import streamlit as st

#main function
def main():

    # Streamlit title 
    st.title("Assisted Summaries")
    st.write("This form uses clustering to assist in generating meaningful summaries of twitter topics.")

    #get inputs
    term = st.text_input("Enter a topic or search term:", " ")
    #term = "abortion"
    clusters = st.number_input(label ="Enter the number of perspectives to find:", 
                                min_value=2, 
                                max_value=5,
                                value=2)

    if term != " ":
        #call API
        with st.spinner("Collectiong Data"):
            #first collect info from API
            r = API_call(term, 50)
            # with open('data3.json', 'w') as f:
            #    json.dump(r, f)

            #with open("data\data3.json", "r", encoding="utf8") as myfile:
            #    r = json.load(myfile)

            # if info is not collected, stop there
            if r == "Oops":
                st.error("Twitter data could not be loaded at this time")
                st.stop()

        #cluster text
        with st.spinner("Clustering Tweets"):
            #initialize models
            gfs = GenFinSummarizer()
            cc = ClusterClass(clusters)

            #prep data and generate embeddings
            work, workdf = gfs.Data_prep(r)
            emb = cc.vectorize_text(work)

            #cluster text
            clusterdf = cc.k_cluster_text(work, emb)

        #generate summaries for clusters
        with st.spinner("Generating Summaries"):
            for i in range(clusters):
                text_list = gfs.make_cloud_chunks(clusterdf[clusterdf['cluster']==i])
                output = gfs.summarize(text_list, length=200)
                st.write("Perspective #"+str(i+1)+":")
                st.write(output)

# Execute main function
if __name__ == "__main__":
    main()
