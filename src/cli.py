import sys
from pathlib import Path
from typing import List, Tuple

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.engine import AgriMatchEngine

# Domain-specific agronomic boundaries used for strict CLI validation
FEATURE_SPECS: List[Tuple[str, str, float, float]] = [
    ("N", "Nitrogen level (N) in soil [0 - 140 kg/ha]", 0.0, 140.0),
    ("P", "Phosphorus level (P) in soil [5 - 145 kg/ha]", 5.0, 145.0),
    ("K", "Potassium level (K) in soil [5 - 205 kg/ha]", 5.0, 205.0),
    ("temperature", "Ambient Temperature [8.0 - 45.0 °C]", 8.0, 45.0),
    ("humidity", "Relative Humidity [14.0 - 100.0 %]", 14.0, 100.0),
    ("ph", "Soil pH level [3.5 - 9.9]", 3.5, 9.9),
    ("rainfall", "Total Rainfall [20.0 - 300.0 mm]", 20.0, 300.0),
]


def prompt_float(prompt_label: str, min_val: float, max_val: float) -> float:
    while True:
        try:
            val_str = input(f"  > {prompt_label:<50}: ").strip()
            val = float(val_str)
            if min_val <= val <= max_val:
                return val
            print(f"    [!] Value out of bounds. Must be between {min_val} and {max_val}.")
        except ValueError:
            print("    [!] Invalid entry. Please enter a valid numerical value.")


def get_fit_label(rank: int) -> str:
    labels = {1: "[Best Fit]", 2: "[Moderate Fit]", 3: "[Alternative]"}
    return labels.get(rank, "[Candidate]")


def run_cli() -> None:
    data_file = Path("data/Crop_recommendation.csv")
    if not data_file.exists():
        print(f"[Error] Dataset file not found at {data_file.resolve()}.")
        sys.exit(1)

    print("Initializing AgriMatch Engine...")
    engine = AgriMatchEngine(data_path=data_file)

    while True:
        print("\n" + "=" * 60)
        print("              AGRIMATCH: PRECISION CROP RECOMMENDER         ")
        print("   Vectorized Distance Engine | Z-Score Standardized        ")
        print("=" * 60 + "\n")

        print("[?] Enter Environmental Parameters:")
        query_vals = []
        for _, label, min_val, max_val in FEATURE_SPECS:
            val = prompt_float(label, min_val, max_val)
            query_vals.append(val)

        results = engine.recommend(query_vals, top_k=3)

        print("\n" + "-" * 60)
        print("                    RECOMMENDED CROPS                       ")
        print("-" * 60)
        print(" Rank | Crop Name       | Match Confidence (Norm Distance) ")
        print("------+-----------------+-----------------------------------")

        for rank, res in enumerate(results, start=1):
            crop_name = str(res["crop"]).capitalize()
            dist = float(res["distance"])
            fit_text = f"{dist:.3f}  {get_fit_label(rank)}"
            print(f"  {rank:02d}  | {crop_name:<15} | {fit_text:<33}")

        print("-" * 60)

        repeat = input("\nRun another query? (y/n): ").strip().lower()
        if repeat not in ("y", "yes"):
            print("\nExiting AgriMatch. Goodbye!")
            break


if __name__ == "__main__":
    run_cli()