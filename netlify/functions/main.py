from mangum import Mangum
from fastapi import FastAPI

app = FastAPI(title="Test API")

@app.get("/")
async def root():
    return {"message": "FastAPI + Netlify Works!", "status": "success"}

@app.get("/docs")
async def docs():
    return {"docs": "Try /simple-api instead"}

@app.get("/simple-api")
async def simple():
    return {"api": "working", "endpoints": ["/", "/simple-api"]}

handler = Mangum(app)
