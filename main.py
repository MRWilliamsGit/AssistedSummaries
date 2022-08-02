from scripts.helpers import API_call
from scripts.summ_class import GenFinSummarizer
import json

def main():
    term = "abortion"
    gfs = GenFinSummarizer()

    #r = API_call(term, 100)
    #print(r)

    #with open('data3.json', 'w') as f:
    #    json.dump(r, f)

    with open('data\data2.json', 'r') as myfile:
        r = json.load(myfile)

    work, workdf = gfs.Data_prep(r)

    text_list = gfs.make_cloud_chunks(workdf)
    output = gfs.summarize(text_list, length=300)

    print(output)


# Execute main function
if __name__ == "__main__":
    main()