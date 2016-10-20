from os.path import isfile, normpath, join as joinpath
from glob import glob           # search for pathnames function

import pandas as pd
from sklearn.model_selection import train_test_split, KFold
# Do stats, and split for cross validation

class Dataset:
    def __init__(self,path, name, ext="txt"):
        self.name = normpath(name)
        self.ext = ext
        self.path = joinpath(path,name) + '/{0}.{1}'
        self.data = None        # Will contain temporarily loaded datasets

    def __len__(self, dataset="all"):
        '''
        Returns the length of dataset
        '''
        if not isfile(self.path.format(dataset, self.ext)):
            return 0
        with open(self.path.format(dataset, self.ext), 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)

    def load(self,dataset="all"):
        self.data = pd.read_csv(self.path.format(dataset,self.ext), sep='\t', header=None)
    
    def append(self, line, dataset="all"):
        '''
        Appends line at the end of the dataset file
        '''
        with open(self.path.format(dataset,self.ext),'a+', encoding='utf-8') as f:
            f.write(line)

    def shuffle(self, dataset="all"):
        '''
        Shuffle dataset and drops duplicates
        '''
        self.load(dataset)
        # http://stackoverflow.com/questions/29576430/shuffle-dataframe-rows
        self.data = self.data.drop_duplicates()
        self.data = self.data.sample(frac=1).reset_index(drop=True)
        self.data.to_csv(self.path.format(dataset,self.ext), sep='\t', header=False, index=False)
        self.data = None
    
    def split(self,train_ratio=0.75):
        '''
        Splits data in all.txt into train and test datasets following ratio specified by train_ratio
        '''
        self.load()
        train, test = train_test_split(self.data, train_size=train_ratio)
        train.loc[:,0] = train[0].apply(lambda s: s.split(',')[0]) # Gives a SettingWithCopyWarning, ... dont know why, might ask on stackoverflow
        self.to_tsv(train, "train")
        self.to_tsv(test, "test")
        self.data = None

    def kfold_split(self, n_splits=2):
        '''
        Split with kfolds for cross validation
        '''
        self.load()
        kf = KFold(n_splits=n_splits)
        count = 0
        for train_index, test_index in kf.split(self.data):
            train, test = self.data.iloc[train_index], self.data.iloc[test_index]
            train.loc[:,0] = train[0].apply(lambda s: s.split(',')[0]) # Gives a SettingWithCopyWarning, ... dont know why, might ask on stackoverflow
            self.to_tsv(train, "train-"+str(count))
            self.to_tsv(test, "test-"+str(count))
            count+=1
        self.data = None

    def join(self, data_path):
        '''
        Joins datasets from all files in data_path
        '''
        for file_path in glob(joinpath(data_path, "*.txt")):
            with open(file_path) as f:
                for l in f:
                    self.append(l)

    def to_tsv(self, data=pd.DataFrame(), name="all"):
        '''
        Print dataframe into csv file
        '''
        if data.empty: data = self.data
        data.to_csv(self.path.format(name,self.ext),
                    sep='\t', header=False, index=False)
                    
    def isLoaded(self):
        '''
        Returns true if data attribute contains a dataset
        '''
        return (self.data is not None)
