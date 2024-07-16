import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader
import os 
import pandas as pd
import numpy as np
import os
import csv
import ast

class EmbeddingsDescriptionsDataset(Dataset):
    def __init__(self, file, root_dir, transform=None):
        self.data = pd.read_csv(os.path.join(root_dir, file))
        self.transform = transform

    def __len__(self):
        return(len(self.data))

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        sample = {'label': ast.literal_eval(self.data.at[idx, 'label']), 'data': ast.literal_eval(self.data.at[idx, 'data'])}
        if self.transform:
            sample = self.transform(sample)

        return sample

class LocalDataLoader():
    def __init__(self):
        self.max_label_length = 0

    def collate_fn(self, batch):
        data = [torch.Tensor(i['data']) for i in batch]
        labels = [torch.Tensor(i['label']) for i in batch]
        labels.append(torch.ones(self.max_label_length))
        # padded_data = pad_sequence(data, batch_first=True, padding_value=0)
        padded_labels = pad_sequence(labels, batch_first=True, padding_value=0)
    
        return torch.stack(data), padded_labels[:-1]

    def determine_max_label_length(self, file, path):
        data = []
        with open(os.path.join(path, file), 'r') as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                data.append(row)
                
        for d in data:
            if len(ast.literal_eval(d['label'])) > self.max_label_length:
                self.max_label_length = len(ast.literal_eval(d['label']))
    
    def get_data_loader(self, file, path):
        self.determine_max_label_length(file, path)
        
        data = EmbeddingsDescriptionsDataset(file, path)

        train_data = DataLoader(data, batch_size=64, shuffle=True, collate_fn=self.collate_fn)

        return train_data
