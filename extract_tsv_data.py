import os
import sys
import pandas as pd

def main():
	corpus_file_path = "/home/nak/muga/annotated_corpus/twitter/SentimentDatasetDaiLabor/de_sentiment_agree2.tsv"
	input_file = pd.read_csv(corpus_file_path, delim_whitespace=True, names=['sentiment', 'tweet'])
	input_file.to_csv('test_output_german.csv')
	

if __name__ == '__main__':
	main()
