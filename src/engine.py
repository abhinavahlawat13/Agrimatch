import csv 
import numpy as np

class Agrimatch:
    def __init__(self,data_path:str):
        self.data_path = data_path
        self.features_name=[
            'N',
            'P',
            'K',
            'temperature',
            'humidity',
            'ph',
            'rainfall'
        ]

        self.X = None
        self.y = None
        self.crop_labels = None
        self.mean = None
        self.std = None

        self.load_and_compute_stats()

    def load_and_compute_stats(self) -> None:
        raw_features=[]
        raw_labels=[]

        #opening the csv file using var self.data_path
        with open(self.data_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) #skipping the header row we only need data not title
            for row in reader:
                #converting the first 7 columns to float and appending to raw_features
                raw_features.append(float(val) for val in row[:7])
                #appending the name of the crop to raw_labels
                raw_labels.append(row[7])