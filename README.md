    # AgriMatch: Precision Crop Recommender

AgriMatch is an interpretable crop recommendation engine built with pure NumPy vectorization and scale-invariant Euclidean distance matching over standardized environmental feature spaces.

## Architecture & Methodology
1. **Z-Score Standardization**: Centers and scales environmental variables ($\mu = 0, \sigma = 1$) so dimensional dominance is eliminated.
2. **Centroid Extraction**: Precomputes ideal agricultural feature centroids across 22 crops using boolean masking.
3. **Broadcasting & Ranking**: Ranks recommendations in $O(1)$ scaling time by evaluating normalized Euclidean norms ($L_2$) against target profiles.

## Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt