# Model Context Protocol (MCP) + AI Foundry + Azure APIM

This project demonstrates a complete deployment of a Model Context Protocol (MCP) system integrated with AI Foundry and Azure API Management (APIM).

## Features
- **MCP Server**: Provides a FastAPI-based backend for weather data and other AI-driven functions.
- **AI Foundry Integration**: Enables AI agents to interact with MCP endpoints using OpenAPI specifications.
- **Azure API Management (APIM)**: Acts as a gateway for secure, managed API access and routing.
- **Container Apps**: Deploys MCP server as a scalable containerized service on Azure.
- **Monitoring & Logging**: Includes APIM policies for request/response logging and monitoring.
- **Deployment Automation**: Scripts and notebooks for end-to-end deployment, including registry setup and OpenAPI generation.

## Main Files
- `main.py`, `simple_mcp_server.py`: MCP server implementation.
- `containerapp.yaml`: Azure Container App deployment configuration.
- `apim_mcp_policy.xml`, `apim_monitoring_policy.xml`: APIM policies for routing and monitoring.
- `mcp-complete-deployment.ipynb`: Notebook for automated deployment and integration steps.
- `openapi-weather.json`: OpenAPI spec for MCP weather API.
- `requirements.txt`: Python dependencies.

## Usage
1. Deploy MCP server as a container app on Azure.
2. Configure APIM gateway for secure API access.
3. Use AI Foundry to connect and interact with MCP endpoints.
4. Monitor and manage API traffic via APIM policies.

## Security
- All secrets and credentials should be masked or stored securely before uploading to GitHub.
- Sensitive files (e.g., registry credentials) should be excluded from version control.

## License
MIT
