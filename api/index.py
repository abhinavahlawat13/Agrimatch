from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

# Add root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.engine import AgriMatchEngine

app = FastAPI()

# Data file path
data_csv = Path(__file__).resolve().parent.parent / "data" / "Crop_recommendation.csv"
engine = AgriMatchEngine(data_path=data_csv)

class QueryRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

@app.post("/api/recommend")
def recommend_crop(data: QueryRequest):
    try:
        query_vector = [
            data.N,
            data.P,
            data.K,
            data.temperature,
            data.humidity,
            data.ph,
            data.rainfall
        ]
        results = engine.recommend(query_vector, top_k=3)
        return {"success": True, "recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
