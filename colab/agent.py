from __future__ import annotations
import os, subprocess
from typing import Any
import httpx
from fastapi import FastAPI, Header, HTTPException

OLLAMA_URL=os.getenv("OLLAMA_URL","http://127.0.0.1:11434")
TOKEN=os.getenv("OLLAMA_STUDIO_TOKEN","")

app=FastAPI(title="Collab Machine Colab Agent")

def auth(value: str|None):
    if TOKEN and value != f"Bearer {TOKEN}": raise HTTPException(401,"invalid token")

async def proxy(method:str,path:str,payload:dict[str,Any]|None=None)->Any:
    async with httpx.AsyncClient(timeout=300) as c:
        r=await c.request(method,f"{OLLAMA_URL}{path}",json=payload)
        r.raise_for_status()
        return r.json()

@app.get("/health")
async def health(authorization:str|None=Header(default=None)):
    auth(authorization)
    try: return {"ok":True,"ollama":True,"models":len((await proxy("GET","/api/tags")).get("models",[]))}
    except Exception as e: return {"ok":True,"ollama":False,"error":str(e)}

@app.get("/api/tags")
async def tags(authorization:str|None=Header(default=None)): auth(authorization); return await proxy("GET","/api/tags")
@app.post("/api/show")
async def show(payload:dict[str,Any],authorization:str|None=Header(default=None)): auth(authorization); return await proxy("POST","/api/show",payload)
@app.post("/api/chat")
async def chat(payload:dict[str,Any],authorization:str|None=Header(default=None)): auth(authorization); return await proxy("POST","/api/chat",payload)
@app.post("/api/generate")
async def generate(payload:dict[str,Any],authorization:str|None=Header(default=None)): auth(authorization); return await proxy("POST","/api/generate",payload)
@app.post("/api/pull")
async def pull(payload:dict[str,Any],authorization:str|None=Header(default=None)): auth(authorization); return await proxy("POST","/api/pull",payload)

@app.get("/gpu")
async def gpu(authorization:str|None=Header(default=None)):
    auth(authorization)
    try:
        r=subprocess.run(["nvidia-smi","--query-gpu=name,memory.total,memory.used,utilization.gpu","--format=csv,noheader,nounits"],capture_output=True,text=True,check=True,timeout=5)
        return {"online":True,"raw":r.stdout.strip()}
    except Exception as e: return {"online":False,"error":str(e)}
