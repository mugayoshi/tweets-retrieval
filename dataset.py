import os
from os.path import isfile
from glob import glob           # search for pathnames function

import pandas as pd
from sklearn.model_selection import train_test_split, KFold
# Do stats, and split for cross validation

class Dataset:
    def __init__(self,path, name, ext=".txt"):
        self.name = name
        self.ext = ext
        self.path = path + name + "/"
        self.data = None        # Will contain temporarily loaded datasets

    def __len__(self, dataset="all"):
        '''
        Returns the length of dataset
        '''
        with open(self.path + dataset + self.ext, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)

    def load(self,dataset="all"):
        self.data = pd.read_csv(self.path + dataset + self.ext, sep='\t', header=None)
    
    def append(self, line, dataset="all"):
        '''
        Appends line at the end of the dataset file
        '''
        with open(self.path + dataset + self.ext,'a', encoding='utf-8') as f:
            f.write(line)

    def shuffle(self, dataset="all"):
        '''
        Shuffle dataset and drops duplicates
        '''
        self.load(dataset)
        # http://stackoverflow.com/questions/29576430/shuffle-dataframe-rows
        self.data = self.data.drop_duplicates()
        self.data = self.data.sample(frac=1).reset_index(drop=True)
        self.data.to_csv(self.path + dataset + self.ext, sep='\t', header=False, index=False)
        self.data = None
    
    def split(self,train_ratio=0.75, n_splits=1):
        '''
        Splits data in all.txt into train and test datasets following ratio specified by train_ratio
        '''
        kf = KFold(n_splits=n_splits)
        for train_index, test_index in kf.split(X):
            print("")
        if self.isTrain() or self.isTest():
            print("There is already a train or test dataset")
        else:
            self.load()
            train, test = train_test_split(self.data, train_size=train_ratio)
            train.loc[:,0] = train[0].apply(lambda s: s.split(',')[0]) # Gives a SettingWithCopyWarning, ... dont know why, might ask on stackoverflow
            train.to_csv(self.path + "train" + self.ext,
                         sep='\t', header=False, index=False)
            test.to_csv(self.path + "test" + self.ext,
                        sep='\t', header=False, index=False)
            self.data = None

    def join(self, data_path):
        '''
        Joins datasets from all files in data_path
        '''
        for filename in glob(data_path + "*.txt"):
            with open(data_path + filename) as f:
                for l in f:
                    d.append(l)
            
    def isLoaded(self):
        '''
        Returns true if data attribute contains a dataset
        '''
        return (self.data is not None)
            
    def isAll(self):
        '''
        Checks whether all data is present or not
        '''
        return isfile(self.path + "all" + self.ext)

    def isTest(self):
        '''
        Checks whether the test data is present or not
        '''
        return isfile(self.path + "test" + self.ext)

    def isTrain(self):
        '''
        Checks whether the train data is present or not
        '''
        return isfile(self.path + "train" + self.ext)
