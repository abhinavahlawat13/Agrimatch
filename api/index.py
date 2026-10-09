from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.engine import AgriMatchEngine

app = FastAPI()

data_csv = ROOT_DIR / "data" / "Crop_recommendation.csv"
engine = AgriMatchEngine(data_path=str(data_csv))

class QueryRequest(BaseModel):
    N: float = Field(..., ge=0, le=140, description="Nitrogen")
    P: float = Field(..., ge=5, le=145, description="Phosphorus")
    K: float = Field(..., ge=5, le=205, description="Potassium")
    temperature: float = Field(..., ge=8.0, le=45.0, description="Temperature")
    humidity: float = Field(..., ge=14.0, le=100.0, description="Humidity")
    ph: float = Field(..., ge=3.5, le=9.9, description="Soil pH")
    rainfall: float = Field(..., ge=20.0, le=300.0, description="Rainfall")

@app.post("/api/recommend")
@app.post("/recommend")
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
