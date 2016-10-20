import io
import random
from os import path

from dataset import Dataset

if __name__ == "__main__":
    dataset_path, data_path = "/home/local/dataset", "/home/local/data"
    dataset_name, data_name = "joint_dataset", "tojoin"

    # Dataset creation
    d = Dataset(dataset_path, dataset_name)
    # d.join(path.join(data_path,data_name))
    # print("Total Length:", len(d))

    # # Dataset manipulation
    # d.shuffle()
    d.split(0.67)
    d.kfold_split(10)
    print("Total Length:", len(d))
    print("Train Length:", d.__len__("train"))
    print("Test Length:", d.__len__("test"))   
    print("Train Length:", d.__len__("train-0"))
    print("Test Length:", d.__len__("test-0"))   
    
