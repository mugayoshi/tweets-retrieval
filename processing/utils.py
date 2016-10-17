import io
import random
import os

from dataset import Dataset

def file_len(path):
    with io.open(path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)


if __name__ == "__main__":
    data_path = "/home/local/data/examples/"
    for dirname in os.listdir(data_path):
        print(dirname)
        d = Dataset(data_path, dirname)
        if d.isTest():
            print("Test is present, making train")
            d.make_train()
