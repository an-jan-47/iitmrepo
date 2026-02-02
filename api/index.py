import json
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Enable CORS for POST from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/")
async def analytics(request: Request):
    body = await request.json()
    regions = body["regions"]
    threshold_ms = body["threshold_ms"]
    
    # Load sample data (in real: upload q-vercel-latency.json to repo as data.json)
    with open("data.json", "r") as f:  # Put q-vercel-latency.json here, rename to data.json
        telemetry = json.load(f)
    
    results = {}
    for region in regions:
        region_data = [r for r in telemetry if r.get("region") == region]
        latencies = np.array([r["latency_ms"] for r in region_data])
        uptimes = [r["uptime"] for r in region_data]
        
        results[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": int(np.sum(latencies > threshold_ms))
        }
    return results
