import json
import pandas as pd
# import matplotlib.pyplot as plt

data_path = "../data/raw.json"

output = []
data_file = open(data_path, "r")
for line in data_file:
    try:
        tweet = json.loads(line)
        print tweet['text']
        print "----------------------------------------"
        output.append(tweet)
    except:
        continue
tweets = pd.DataFrame(output)

