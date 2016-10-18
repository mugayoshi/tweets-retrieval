import os
import io

# from plot import ..

class Dataset:
    def __init__(self,path, name, ext=".txt",train="train",test="test"):
        self.name = name
        self.ext = ext
        self.path = path + name + "/"
        
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
    
    def make_train(self):
        '''
        Makes train dataset from test
        '''
        if self.isTrain():
            print("There is already a train dataset")
        else:
            with io.open(self.path + "test" + self.ext,'r', encoding='utf-8') as in_file, io.open(self.path + "train" + self.ext, 'w',encoding='utf-8') as out_file:
                for in_line in in_file:
                    (yc, Xc) = in_line.rstrip('\n').split('\t')
                    print(yc.split(',')[0] + '\t' + Xc, file=out_file)

    
    def test_size(self,f):
        '''
        Returns the size of the test data
        '''
        return file_len(self.path + "test" + self.ext)

    def train_size(self,f):
        '''
        Returns the size of the test data
        '''
        return file_len(self.path + "train" + self.ext)
    
  
    # def randomize(d,)
    # import pandas as pd
    # # Retrieve data from raw file
    # df = pd.DataFrame.from_csv(input['path'] + input['extension'], sep='\t')
    # # Keep only tweets contents
    # df = df["tweet"][6:]
    # # Save in new file
    # df.to_csv(output['path'] + output['extension'], index=False)
