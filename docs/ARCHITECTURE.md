# System Architecture & Technical Flow

## 1. System Pipeline Flowchart

```text
+------------------------------------+
|  Raw Dataset                       |
|  Crop_recommendation.csv           |
|  Shape: (2200, 7) + Labels (2200,) |
+------------------+-----------------+
                   |
                   v
+------------------------------------+
|  1. Global Standardization         |
|     Compute mu (7,) & sigma (7,)   |
|     Z = (X - mu) / sigma           |
+------------------+-----------------+
                   |
                   v
+------------------------------------+
|  2. Crop Centroid Computation      |
|     Boolean Masking: (y == crop)   |
|     Output: Centroids (22, 7)      |
+------------------+-----------------+
                   |
                   | <------------------------- [ User Query Vector (7,) ]
                   v                                    |
+------------------------------------+                  |
|  3. Vectorized Inference           |                  v
|     Normalize Query Vector         +<--- Z_query = (q - mu) / sigma
|     Broadcasted Subtraction        |
|     Euclidean Norm: np.linalg.norm |
+------------------+-----------------+
                   |
                   v
+------------------------------------+
|  4. Ranking & Selection            |
|     np.argsort(distances)          |
|     Top-K Crop Recommendations     |
+------------------------------------+
Query Vector (q_scaled):
[ z_N, z_P, z_K, z_temp, z_hum, z_ph, z_rain ]  --> Shape: (1, 7)
                       |
                       |  NumPy Auto-Broadcasting
                       v
Target Centroid Matrix (Profiles):
┌  Rice       : [ c1, c2, c3, c4, c5, c6, c7 ] ┐
│  Maize      : [ c1, c2, c3, c4, c5, c6, c7 ] │
│  Chickpea   : [ c1, c2, c3, c4, c5, c6, c7 ] │ --> Shape: (22, 7)
│  ...        : [ ..  ..  ..  ..  ..  ..  .. ] │
└  Cotton     : [ c1, c2, c3, c4, c5, c6, c7 ] ┘
                       |
                       v  Vectorized Difference: (Profiles - q_scaled)
                       |  Euclidean Norm: ||Profiles - q_scaled||_2
                       v
Distance Vector:
[ d_Rice, d_Maize, d_Chickpea, ..., d_Cotton ]  --> Shape: (22,)
                       |
                       v  np.argsort()
Top 3 Recommended Crops (Sorted by minimum distance)


Agrimatch/
├── data/
│   └── Crop_recommendation.csv
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DESIGN.md
│   ├── MEMORY.md
│   ├── PRD.md
│   ├── RULES.md
│   └── TASKS.md
├── src/
│   ├── __init__.py
│   ├── cli.py
│   └── engine.py
├── .gitignore
├── README.md
└── requirements.txt