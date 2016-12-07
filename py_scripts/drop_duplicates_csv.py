from csv import QUOTE_NONE
import pandas as pd

input_path = "/home/muga/twitter/new_trainingdata/temp/en_merge_2columns.csv"
input_path_de = "/home/muga/twitter/new_trainingdata/temp/de_merge_2columns.csv"
input_path_fr = "/home/muga/twitter/new_trainingdata/temp/fr_merge_2columns.csv"
output_path = "/home/muga/twitter/new_trainingdata/temp/en_merge_uniq.csv"
output_path_de = "/home/muga/twitter/new_trainingdata/temp/de_merge_uniq.csv"
output_path_fr = "/home/muga/twitter/new_trainingdata/temp/fr_merge_uniq.csv"

d = pd.read_csv(input_path_fr, sep=',', header=None, names=["sentiment", "content"])
# dtype=str,# quoting=QUOTE_NONE
d.drop_duplicates()
# d = d.sample(frac=1).reset_index(drop=True)

d.to_csv(output_path_fr,
         sep=',',
         header=False,
         index=False,
         # quoting=QUOTE_NONE
)

