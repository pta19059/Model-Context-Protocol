from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import uvicorn

app = FastAPI(title="MCP Weather Server", version="1.0.0")

# CORS per permettere chiamate da APIM
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dati weather statici
weather_data = {
    "milan": {"temperature": 22, "condition": "Sunny", "humidity": 65},
    "rome": {"temperature": 28, "condition": "Partly Cloudy", "humidity": 70},
    "london": {"temperature": 15, "condition": "Rainy", "humidity": 85},
    "lisbon": {"temperature": 25, "condition": "Clear", "humidity": 60}
}

class JSONRPCRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int = 1

class JSONRPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: dict = {}
    id: int = 1

@app.get("/")
def root():
    return {"message": "MCP Weather Server is running", "status": "healthy"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "mcp-weather"}

@app.post("/")
def handle_jsonrpc(request: JSONRPCRequest):
    if request.method == "get_weather":
        city = request.params.get("city", "milan").lower()

        if city in weather_data:
            weather_info = weather_data[city]
            return JSONRPCResponse(
                result={
                    "city": city.title(),
                    "temperature": f"{weather_info['temperature']}°C",
                    "condition": weather_info["condition"],
                    "humidity": f"{weather_info['humidity']}%"
                },
                id=request.id
            )
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": "City not found"},
                "id": request.id
            }

    return {
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Method not found"},
        "id": request.id
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
