import torch
import pandas as pd
import numpy as np
from torch.utils import data

class AbstractDataset(data.Dataset):
  def __init__(self, data,  list_IDs: list, labels: dict):
        """Create custom torch Dataset.
        
        Arguments:
            data {array-like} --  DataFrame containing dataset.
            list_IDs {list} -- List of data IDs to be loaded.
            labels {dict} -- Map of data IDs to their labels.
        
        Returns:
            X, y -- data and label.
        """
        self.data = data
        self.labels = labels
        self.list_IDs = list_IDs

  def __len__(self):
        return len(self.list_IDs)

  def __getitem__(self, index):
        # Select sample
        ID = self.list_IDs[index]

        # Load data and get label
        X = self.data[self.data[0] == ID][1].values
        y = self.labels[ID]
        print(X, type(X))
        return torch.Tensor(X), torch.Tensor(y)