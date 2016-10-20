import io
import random
from os.path import join

from dataset import Dataset

if __name__ == "__main__":
    dataset_path = "/home/local/dataset/"
    data_path = "/home/local/data/"
    dataset_name = "twitter_dataset_1"

    # Dataset creation
    d = Dataset(dataset_path, dataset_name)
    d.join(data_path + "examples")
    print("Total Length:", len(d))

    # Dataset manipulation
    print("All,Test,Train:",d.isAll(), d.isTest(),d.isTrain())
    d.shuffle()
    d.split()
    print("Total Length:", len(d))
    print("Train Length:", d.__len__("train"))
    print("Test Length:", d.__len__("test"))   
    
