import os
import io

import pandas as pd
from sklearn.model_selection import train_test_split
# from plot import ..

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
        with io.open(self.path + dataset + self.ext, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)

    def load(self,dataset="all"):
        self.data = pd.read_csv(self.path + dataset + self.ext, sep='\t', header=None)
    
    def append(self, line, dataset):
        '''
        Appends line at the end of the dataset file
        '''
        with io.open(self.path + dataset + self.ext,'a', encoding='utf-8') as f:
            print(line, file=f)

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
    
    def split(self,train_ratio=0.75):
        '''
        Splits data in all.txt into train and test datasets following ratio specified by train_ratio
        '''
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
        
    def isLoaded(self):
        '''
        Returns true if data attribute contains a dataset
        '''
        return (self.data is not None)
            
    def isAll(self):
        '''
        Checks whether all data is present or not
        '''
        return os.path.isfile(self.path + "all" + self.ext)

    def isTest(self):
        '''
        Checks whether the test data is present or not
        '''
        return os.path.isfile(self.path + "test" + self.ext)

    def isTrain(self):
        '''
        Checks whether the train data is present or not
        '''
        return os.path.isfile(self.path + "train" + self.ext)
