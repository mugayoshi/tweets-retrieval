import io
import random
import os

from dataset import Dataset

if __name__ == "__main__":
    data_path = "/home/local/data/examples/"
    # for dirname in os.listdir(data_path):
    #     print(dirname)
    #     d = Dataset(data_path, dirname)
    #     if d.isTest():
    #         print("Test is present, making train")
    #         d.make_train()
    d = Dataset(data_path, "19294-nobel_prize_cell_science_chemistry_research")
    print("All,Test,Train:",d.isAll(), d.isTest(),d.isTrain())
    d.shuffle()
    d.split()
    print("Total Length:", len(d))
    print("Train Length:", d.__len__("train"))
    print("Test Length:", d.__len__("test"))
    
