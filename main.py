from scripts.helpers import API_call, Data_prep
from scripts.summ_class import GenFinSummarizer
import json

def main():
    term = "abortion"
    gfs = GenFinSummarizer()

    #r = API_call(term, 10)
    #print(r)

    #with open('data2.json', 'w') as f:
    #    json.dump(r, f)

    with open('data2.json', 'r') as myfile:
        r = json.load(myfile)

    work, workdf = Data_prep(r)

    text_list = gfs.make_cloud_chunks(workdf)
    output = gfs.summarize(text_list, length=400)

    print(output)


# Execute main function
if __name__ == "__main__":
    main()