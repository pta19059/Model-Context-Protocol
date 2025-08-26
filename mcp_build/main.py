from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return jsonify({"service": "mcp-weather-server", "status": "running", "version": "1.0"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "mcp-weather-server"})

@app.route('/mcp/tools/call', methods=['POST'])
def mcp_tools_call():
    try:
        data = request.get_json() or {}
        location = data.get('params', {}).get('arguments', {}).get('location', 'Unknown')

        # Simulate weather data
        weather_response = {
            "jsonrpc": "2.0",
            "result": {
                "content": [{
                    "type": "text", 
                    "text": f"Weather in {location}: Sunny, 22C, Light breeze. Perfect day for outdoor activities!"
                }]
            },
            "id": data.get('id', '1')
        }

        return jsonify(weather_response)
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
            "id": "1"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)