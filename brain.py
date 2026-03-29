from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import uvicorn

app = FastAPI(title="Mini-Mesh Brain")

class Peer(BaseModel):
    name: str
    public_key: str
    local_ip: str
    virtual_ip: str = ""

# Simple in-memory database
# In a production app, use SQLite or similar
peers_db: Dict[str, Peer] = {}
next_ip_suffix = 2  # Start assigning from 10.0.0.2

@app.post("/register")
async def register(peer: Peer):
    global next_ip_suffix
    
    # If peer already exists, just update its details but keep the Virtual IP
    if peer.name in peers_db:
        existing = peers_db[peer.name]
        peer.virtual_ip = existing.virtual_ip
    else:
        # Assign a new Virtual IP in the 10.0.0.x range
        peer.virtual_ip = f"10.0.0.{next_ip_suffix}"
        next_ip_suffix += 1
    
    peers_db[peer.name] = peer
    print(f"Registered {peer.name} at {peer.local_ip} (Virtual IP: {peer.virtual_ip})")
    return {"status": "ok", "virtual_ip": peer.virtual_ip}

@app.get("/peers", response_model=List[Peer])
async def get_peers():
    return list(peers_db.values())

if __name__ == "__main__":
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
