from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add the parent directory and mcp-tools directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, "mcp-tools"))

import tools
from mcp_client_agent import get_agent_response
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/contracts")
def api_list_contracts():
    return tools.list_contracts()

@app.get("/api/contracts/all/metadata")
def api_get_all_metadata():
    contracts = tools.list_contracts()
    data = []
    for c in contracts:
        metadata = tools.get_contract_metadata(c)
        data.append(metadata)
    return data

@app.get("/api/contracts/{filename}/metadata")
def api_get_metadata(filename: str):
    return tools.get_contract_metadata(filename)

@app.get("/api/contracts/{filename}/analyze")
def api_get_analysis(filename: str):
    result = tools.analyze_contract(filename)
    return {"analysis": result}

class ChatRequest(BaseModel):
    query: str
    history: list = None

@app.post("/api/chat")
def api_chat(request: ChatRequest):
    response = get_agent_response(request.query, request.history)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
