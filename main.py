from scripts.helpers import API_call
from scripts.clustering_class import ClusterClass
from scripts.summary_class import GenFinSummarizer
import json
import streamlit as st


def main():

    # Streamlit title 
    st.title("Assisted Summaries")
    st.write("This form uses clustering to assist in generating meaningful summaries of twitter topics.")

    # Create search functionality
    #term = st.text_input("Enter a subject", " ")
    term = "abortion"

    gfs = GenFinSummarizer()
    cc = ClusterClass()

    # r = API_call(term, 100)
    # print(r)

    # with open('data3.json', 'w') as f:
    #    json.dump(r, f)

    with open("data\data2.json", "r", encoding="utf8") as myfile:
        r = json.load(myfile)

    work, workdf = gfs.Data_prep(r)

    emb = cc.vectorize(work)
    cc.cluster_text(work, emb)

    #text_list = gfs.make_cloud_chunks(workdf)
    #output = gfs.summarize(text_list, length=300)
    #print(output)


# Execute main function
if __name__ == "__main__":
    main()
