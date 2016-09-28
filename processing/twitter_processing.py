import sys
import codecs
import json
import pandas as pd
# import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) > 2:
        json_path = sys.argv[1]
        output_path = sys.argv[2]
    else:
        print "No raw data path and output path specified in arguments."
        exit()
    output = []
    json_file = open(json_path, "r")
    for line in json_file:
        try:
            tweet = json.loads(line)
            output.append(tweet['text'].replace('\n',''))
        except:
            continue
    # tweets = pd.DataFrame(output)
    print "ok"
    output_file = codecs.open(output_path, "w+", encoding="utf-8")
    for tweet in output:
        output_file.write("%s\n" % tweet)
        

