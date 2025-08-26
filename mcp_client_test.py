#!/usr/bin/env python3
"""
MCP Client Test - Direct testing of real MCP server
"""
import requests
import json

MCP_SERVER_URL = "https://mcp-weather-1onhmd.purpleflower-1b791e7b.eastus.azurecontainerapps.io"

def test_mcp_capabilities():
    """Test MCP capabilities endpoint"""
    response = requests.get(f"{MCP_SERVER_URL}/mcp/capabilities")
    print("Capabilities:", response.json())

def test_mcp_weather_tool(location="lisbona"):
    """Test MCP weather tool call"""
    tool_request = {
        "jsonrpc": "2.0",
        "id": "test-weather",
        "method": "tools/call",
        "params": {
            "name": "get_weather",
            "arguments": {"location": location}
        }
    }

    response = requests.post(f"{MCP_SERVER_URL}/mcp/tools/call", json=tool_request)
    print(f"Weather for {location}:", response.json())

if __name__ == "__main__":
    print("🧪 Testing Real MCP Server...")
    test_mcp_capabilities()
    test_mcp_weather_tool("lisbona")
    test_mcp_weather_tool("milan")
