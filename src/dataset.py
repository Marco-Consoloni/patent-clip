import json
import os
from PIL import Image
from enum import Enum

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

from transformers import CLIPProcessor

from src.config import get_cfg

class PatentDatasetType(Enum):
    TRAIN = "train"
    VALIDATION = "eval"
    TEST = "test"

class PatentDataset(Dataset):
    def __init__(self, type):
        assert isinstance(type, PatentDatasetType), "type must be PatentDatasetType"
        self.cfg = get_cfg()
        
        self.path = os.path.join(self.cfg.dataset.path, type.value)
        self.processor = CLIPProcessor.from_pretrained(self.cfg.model.base)
        self.files = os.listdir(self.path)

    def __len__(self):
        return len(self.files) if not self.cfg.debug else 1024

    def __getitem__(self, idx):
        fname = os.path.join(self.path, self.files[idx])
        with open(fname, "r") as f:
            metadata = json.load(f)
        
        text = metadata[self.cfg.dataset.fields.text]
        image_path = metadata[self.cfg.dataset.fields.image]
        image = Image.open(image_path)

        inputs = self.processor(
            text=[text],
            images=image,
            return_tensors="pt",
            truncation=True,
            padding='max_length',
            max_length=self.cfg.model.max_length
        )

        return dict(
            input_ids=inputs["input_ids"][0],
            attention_mask=inputs["attention_mask"][0],
            pixel_values=inputs["pixel_values"][0]
        )

if __name__ == "__main__":
    train_ds = PatentDataset(PatentDatasetType.TRAIN)
    val_ds = PatentDataset(PatentDatasetType.VALIDATION)
    test_ds = PatentDataset(PatentDatasetType.TEST)

    print(len(train_ds))
    print(len(val_ds))
    print(len(test_ds))
    
    ds = PatentDataset(PatentDatasetType.VALIDATION)
    #print(list(ds[0].keys()))
    #print(ds[0].input_ids.shape)
    #print(ds[1].input_ids.shape)
    
    dl = DataLoader(ds, batch_size=4, shuffle=False)
    elem = next(iter(dl))
    #print(elem)