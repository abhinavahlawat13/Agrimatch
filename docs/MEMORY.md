# Project Memory & Architecture Log

## Implemented Architecture
- **Scale Standardization**: Features are normalized using global Z-scores ($Z = \frac{X - \mu}{\sigma}$) to prevent high-magnitude features (e.g., rainfall up to 300 mm) from dominating low-magnitude features (e.g., pH scale 3.5–9.9). Zero-variance protection with epsilon ($10^{-8}$) is enforced.
- **Profiling via Centroids**: Built an exact $(22, 7)$ target centroid profile matrix using NumPy boolean masking over unique crop labels.
- **Inference Math**: User inputs are projected into the standardized space. Vectorized difference computation is performed via auto-broadcasting, and $L_2$ Euclidean distances ($\Vert{}\text{centroids} - q_{\text{scaled}}\Vert{}_2$) are ranked via `np.argsort`.
- **Runtime Compatibility**: Used `typing.Union` instead of PEP 604 pipe syntax (`|`) to maintain backward compatibility across Python 3.8, 3.9, and 3.10+.
- **CLI Guardrails**: Enforced agronomic boundary validation for all 7 input features before computing distances.