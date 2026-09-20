# Product Requirements Document (PRD) - AgriMatch

## 1. Problem Statement
Farmers and agriculturalists often rely on intuition or uncalibrated soil tests to choose crops. High-dimensional environmental variables (N, P, K, rainfall, pH, temperature, humidity) make manual matching inefficient and error-prone.

## 2. Target User
- Precision agriculture enthusiasts, agronomy researchers, and software engineers seeking an interpretable, mathematically sound crop recommendation engine.

## 3. Core Goals
- Vectorized crop profile generation from historical data.
- Instant, calibrated matching using Euclidean distance over Z-score standardized feature spaces.
- Interactive CLI with input validation.

## 4. Core Features
- Z-score normalization to prevent feature scale dominance (e.g., rainfall overpowering pH).
- Crop centroid matrix generation (22 unique crops, 7 features each).
- Top-K ranked recommendation output with confidence/distance metric.