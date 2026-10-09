from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.engine import AgriMatchEngine

app = FastAPI(title="AgriMatch")

# Initialize engine with dataset
data_csv = ROOT_DIR / "data" / "Crop_recommendation.csv"
engine = AgriMatchEngine(data_path=str(data_csv))

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AgriMatch - Precision Crop Recommender</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col items-center py-10 px-4 font-sans">
  <div class="max-w-2xl w-full bg-white rounded-2xl shadow-lg border border-slate-100 p-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold tracking-tight text-emerald-700">🌱 AgriMatch</h1>
      <p class="text-sm text-slate-500 mt-1">Vectorized Distance Engine | Z-Score Standardized</p>
    </div>

    <form id="cropForm" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-xs font-semibold text-slate-600 mb-1">Nitrogen (N) [0-140]</label>
        <input type="number" step="any" id="N" value="90" class="w-full border rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" required>
      </div>
      <div>
        <label class="block text-xs font-semibold text-slate-600 mb-1">Phosphorus (P) [5-145]</label>
        <input type="number" step="any" id="P" value="42" class="w-full border rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" required>
      </div>
      <div>
        <label class="block text-xs font-semibold text-slate-600 mb-1">Potassium (K) [5-205]</label>
        <input type="number" step="any" id="K" value="43" class="w-full border rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" required>
      </div>
      <div>
        <label class="block text-xs font-semibold text-slate-600 mb-1">Temperature (°C) [8-45]</label>
        <input type="number" step="any" id="temp" value="20.8" class="w-full border rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" required>
      </div>
      <div>
        <label class="block text-xs font-semibold text-slate-600 mb-1">Humidity (%) [14-100]</label>
        <input type="number" step="any" id="humidity" value="82.0" class="w-full border rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" required>
      </div>
      <div>
        <label class="block text-xs font-semibold text-slate-600 mb-1">Soil pH [3.5-9.9]</label>
        <input type="number" step="any" id="ph" value="6.5" class="w-full border rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" required>
      </div>
      <div class="md:col-span-2">
        <label class="block text-xs font-semibold text-slate-600 mb-1">Rainfall (mm) [20-300]</label>
        <input type="number" step="any" id="rainfall" value="202.9" class="w-full border rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 outline-none" required>
      </div>
      <div class="md:col-span-2 mt-4">
        <button type="submit" id="submitBtn" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3 rounded-lg shadow transition">
          Get Recommendations
        </button>
      </div>
    </form>

    <div id="results" class="mt-8 hidden">
      <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3">Top Recommendations</h3>
      <div id="cardsList" class="space-y-3"></div>
    </div>
  </div>

  <script>
    document.getElementById('cropForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      btn.innerText = 'Calculating...';
      btn.disabled = true;

      const payload = {
        N: parseFloat(document.getElementById('N').value),
        P: parseFloat(document.getElementById('P').value),
        K: parseFloat(document.getElementById('K').value),
        temperature: parseFloat(document.getElementById('temp').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        ph: parseFloat(document.getElementById('ph').value),
        rainfall: parseFloat(document.getElementById('rainfall').value)
      };

      try {
        let endpoint = '/api/recommend';
        let res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!res.ok) {
          endpoint = '/recommend';
          res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        }

        const data = await res.json();
        if (data.success) {
          const cardsList = document.getElementById('cardsList');
          cardsList.innerHTML = '';
          const badges = ['Best Fit', 'Moderate Fit', 'Alternative'];
          const colors = [
            'bg-emerald-50 border-emerald-300 text-emerald-800',
            'bg-blue-50 border-blue-200 text-blue-800',
            'bg-slate-50 border-slate-200 text-slate-700'
          ];
          
          data.recommendations.forEach((item, index) => {
            cardsList.innerHTML += `
              <div class="flex items-center justify-between border rounded-xl p-4 ${colors[index]}">
                <div>
                  <span class="text-xs uppercase font-bold tracking-wider opacity-70">#0${index + 1} Recommendation</span>
                  <h4 class="text-lg font-bold capitalize">${item.crop}</h4>
                </div>
                <div class="text-right">
                  <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-white/80 border">${badges[index]}</span>
                  <p class="text-xs mt-1 text-slate-500">Distance: ${item.distance.toFixed(3)}</p>
                </div>
              </div>
            `;
          });
          document.getElementById('results').classList.remove('hidden');
        } else {
          alert('Error: ' + JSON.stringify(data));
        }
      } catch (err) {
        alert('Request failed: ' + err.message);
      } finally {
        btn.innerText = 'Get Recommendations';
        btn.disabled = false;
      }
    });
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
@app.get("/api/", response_class=HTMLResponse)
def home():
    return HTML_CONTENT

class QueryRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

@app.post("/recommend")
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