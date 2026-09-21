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
                raw_features.append([float(val) for val in row[:7]])
                #appending the name of the crop to raw_labels
                raw_labels.append(row[7])

        # Convert to pure NumPy arrays
        self.X = np.array(raw_features, dtype=np.float64)
        self.y = np.array(raw_labels)
        self.crop_labels = np.unique(self.y)

        # Compute mean and standard deviation for Z-score normalization
        self.mean = np.mean(self.X, axis=0)
        self.std = np.std(self.X, axis=0)

        # Prevent division by zero if std is zero
        self.std[self.std == 0] = 1.0

        # Compute centroids using boolean masking
        X_norm = (self.X - self.mean) / self.std
        self.centroids = {}
        for crop in self.crop_labels:
            mask = self.y == crop
            self.centroids[crop] = np.mean(X_norm[mask], axis=0)