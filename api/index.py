from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sys
from pathlib import Path

# Root path add karo
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.engine import AgriMatchEngine

app = FastAPI()

# Data initialize
data_csv = ROOT_DIR / "data" / "Crop_recommendation.csv"
engine = AgriMatchEngine(data_path=data_csv)

class QueryRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

@app.get("/", response_class=HTMLResponse)
def serve_home():
    html_file = ROOT_DIR / "public" / "index.html"
    if html_file.exists():
        return html_file.read_text(encoding="utf-8")
    return "<h1>AgriMatch UI file missing</h1>"

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
