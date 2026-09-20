# Design System & UI Architecture (CLI)

## 1. Interaction State Flow

```text
   [ Start CLI Application ]
               |
               v
    +----------------------+
    | Load AgriMatch Engine|
    | Compute Centroids    |
    +----------+-----------+
               |
               v
+------------> [ Input Prompt ] <--------------+
|              Prompt for Feature (1 of 7)     |
|                      |                       |
|                      v                       |
|              { Valid Float? }                |
|               /            \                 |
|             No              Yes              |
|             /                \               |
|   [ Show Error Alert ]    [ Append Value ]   |
|            |                 |               |
|            +-----------------+               |
|                              |               |
|                    { All 7 Gathered? }       |
|                       /            \         |
|                     No              Yes      |
|                     /                \       |
|                    +                  v      |
+---------------------------------------+      |
                                               |
                                               v
                                    +--------------------+
                                    | Compute Distances  |
                                    | Format Recommendations
                                    +----------+---------+
                                               |
                                               v
                                    +--------------------+
                                    | Print Result Table |
                                    +----------+---------+
                                               |
                                               v
                                       { Run Again? }
                                       /            \
                                     Yes             No
                                     /                \
                                    +                  v
                                                  [ Exit CLI ]
```

---

## 2. Terminal UI Wireframe

```text
============================================================
              AGRIMATCH: PRECISION CROP RECOMMENDER         
   Vectorized Distance Engine | Z-Score Standardized        
============================================================

[?] Enter Environmental Parameters:
  > Nitrogen level (N) in soil [0 - 140 kg/ha]       : 90
  > Phosphorus level (P) in soil [5 - 145 kg/ha]     : 42
  > Potassium level (K) in soil [5 - 205 kg/ha]      : 43
  > Ambient Temperature [8.0 - 45.0 °C]              : 20.8
  > Relative Humidity [14.0 - 100.0 %]               : 82.0
  > Soil pH level [3.5 - 9.9]                        : 6.5
  > Total Rainfall [20.0 - 300.0 mm]                 : 202.9

------------------------------------------------------------
                    RECOMMENDED CROPS                       
------------------------------------------------------------
 Rank | Crop Name       | Match Confidence (Norm Distance) 
------+-----------------+-----------------------------------
  01  | Rice            | 0.312  [Best Fit]
  02  | Jute            | 1.487  [Moderate Fit]
  03  | Papaya          | 2.190  [Alternative]
------------------------------------------------------------
```