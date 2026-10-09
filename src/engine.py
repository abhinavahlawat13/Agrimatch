from pathlib import Path
from typing import Dict, List, Union
import numpy as np


class AgriMatchEngine:
    FEATURE_NAMES: List[str] = [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "ph",
        "rainfall",
    ]

    def __init__(self, data_path: Union[str, Path] = "data/Crop_recommendation.csv") -> None:
        self.data_path = Path(data_path)
        self.X: np.ndarray
        self.y: np.ndarray
        self.mu: np.ndarray
        self.sigma: np.ndarray
        self.unique_crops: np.ndarray
        self.centroids: np.ndarray

        self._load_and_prepare_data()

    def _load_and_prepare_data(self) -> None:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found at: {self.data_path}")

        # Load raw data without heavy ML frameworks using pure NumPy
        data = np.genfromtxt(
            self.data_path,
            delimiter=",",
            dtype=str,
            skip_header=1,
        )

        self.X = data[:, :7].astype(np.float64)
        self.y = data[:, 7]

        # Calculate global mu and sigma for scale-invariant Z-score standardization
        self.mu = np.mean(self.X, axis=0)
        self.sigma = np.std(self.X, axis=0, ddof=0)
        self.sigma = np.where(self.sigma == 0, 1e-8, self.sigma)

        # Standardize features so high-magnitude units (e.g. rainfall) do not dominate pH/NPK
        X_scaled = (self.X - self.mu) / self.sigma

        # Compute crop centroid profiles via boolean masking
        self.unique_crops = np.unique(self.y)
        centroids_list = []

        for crop in self.unique_crops:
            mask = self.y == crop
            crop_centroid = np.mean(X_scaled[mask], axis=0)
            centroids_list.append(crop_centroid)

        # Centroid matrix shape: (22 crops, 7 features)
        self.centroids = np.vstack(centroids_list)

    def recommend(self, query: Union[List[float], np.ndarray], top_k: int = 3) -> List[Dict[str, Union[float, str]]]:
        q = np.asarray(query, dtype=np.float64).flatten()
        if q.shape[0] != 7:
            raise ValueError(f"Expected query of length 7, got {q.shape[0]}")

        # Project user query into the calibrated Z-score feature space
        q_scaled = (q - self.mu) / self.sigma

        # Vectorized Euclidean distance across all crop centroids using broadcasting
        diff = self.centroids - q_scaled
        distances = np.linalg.norm(diff, axis=1)

        # Rank recommendations by minimum distance (highest match confidence)
        sorted_indices = np.argsort(distances)[:top_k]

        return [
            {
                "crop": str(self.unique_crops[idx]),
                "distance": float(distances[idx]),
            }
            for idx in sorted_indices
        ]