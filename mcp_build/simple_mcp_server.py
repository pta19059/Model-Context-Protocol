import json
from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Weather API configuration (using a free service)
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
# Using a demo key - in production, use a real API key
WEATHER_API_KEY = "demo"

def get_weather_data(location):
    """Simulate weather data for MCP demonstration"""
    # In a real implementation, you would call an actual weather API
    # For demo purposes, return simulated data
    demo_weather = {
        "location": location.title(),
        "temperature": "22°C",
        "condition": "Sunny",
        "humidity": "65%",
        "wind_speed": "15 km/h",
        "timestamp": datetime.now().isoformat()
    }

    return {
        "weather": demo_weather,
        "source": "Demo Weather Service",
        "mcp_protocol": "2024-11-05"
    }

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "MCP Weather Server",
        "protocol": "2024-11-05",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/', methods=['GET', 'POST'])
def mcp_root():
    """MCP server root endpoint"""
    if request.method == 'GET':
        return jsonify({
            "protocol": "Model Context Protocol",
            "version": "2024-11-05",
            "server": "MCP Weather Server",
            "capabilities": ["tools"],
            "tools": ["get_weather"]
        })

    # Handle JSON-RPC requests
    try:
        data = request.get_json()
        if not data or 'method' not in data:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -32600, "message": "Invalid Request"},
                "id": data.get('id') if data else None
            }), 400

        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id', 'unknown')

        if method == 'tools/call':
            tool_name = params.get('name')
            arguments = params.get('arguments', {})

            if tool_name == 'get_weather':
                location = arguments.get('location', 'unknown')
                weather_result = get_weather_data(location)

                return jsonify({
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Weather for {weather_result['weather']['location']}: {weather_result['weather']['temperature']}, {weather_result['weather']['condition']}. Humidity: {weather_result['weather']['humidity']}, Wind: {weather_result['weather']['wind_speed']}"
                            }
                        ],
                        "isError": False
                    },
                    "id": request_id
                })
            else:
                return jsonify({
                    "jsonrpc": "2.0",
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                    "id": request_id
                }), 404
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Unknown method: {method}"},
                "id": request_id
            }), 404

    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
            "id": request.get_json().get('id') if request.get_json() else None
        }), 500

@app.route('/mcp/tools/call', methods=['POST'])
def mcp_tools_call():
    """Direct MCP tools endpoint for APIM integration"""
    try:
        data = request.get_json()
        method = data.get('method', 'tools/call')
        params = data.get('params', {})
        request_id = data.get('id', 'mcp-request')

        tool_name = params.get('name')
        arguments = params.get('arguments', {})

        if tool_name == 'get_weather':
            location = arguments.get('location', 'unknown')
            weather_result = get_weather_data(location)

            return jsonify({
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Weather for {weather_result['weather']['location']}: {weather_result['weather']['temperature']}, {weather_result['weather']['condition']}. Humidity: {weather_result['weather']['humidity']}, Wind: {weather_result['weather']['wind_speed']}"
                        }
                    ],
                    "isError": False
                },
                "id": request_id
            })
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                "id": request_id
            }), 404

    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
            "id": request_id
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
