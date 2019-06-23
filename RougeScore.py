import json
import wikipedia
import requests
from rouge import Rouge

with open("/home/wang1292/Documents/genSummaries.txt") as f:
    cdata = json.load(f)

json_data = requests.get("https://www.forbes.com/ajax/list/data?year=2017&uri=power-women&type=person").content.decode('utf-8')
data = [item for item in json.loads(json_data)]
names = []
for item in data:
    names.append(item["name"])

rouge = Rouge()
scores = []
for name in names:
    try:
        if cdata[name]:
            ref = wikipedia.summary(name)
            print("Retrieve " + name + "success.\n")
            #corefHyp = cdata[name]
            genHyp = cdata[name]
            genSentence = " ".join(genHyp)
            scores.append(rouge.get_scores(genSentence, ref, avg=True))
            print("Append score success.")



    except Exception as e:
        print("key not exist\n")


with open("/home/wang1292/Documents/scores1.txt", 'w') as json_file:
    json.dump(scores, json_file)