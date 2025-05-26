# MCP Server for CTERA Edge

**mcp-ctera-edge** provides an AI-powered interface to interact with the CTERA Edge Filer, using Model Context Protocol (MCP). This integration enables access to the file management APIs of CTERA Edge, allowing you to perform operations through natural language or automation workflows.

---

## 🔧 Features

- Integration with CTERA Edge APIs for file and folder management
- AI-driven command execution via MCP
- Support for SSL/non-SSL connections
- Comprehensive file operations: list, create, copy, move, delete
- Easily extensible to support more CTERA Edge functions

---

## 🚀 Getting Started

To run this server, ensure you have the [MCP runtime](https://modelcontextprotocol.io/quickstart/user) installed and follow the configuration steps below.

---

## 🧩 MCP Server Configuration

Configuration using Standard I/O:

```json
{
    "mcpServers": {
      "ctera-edge": {
        "command": "uv",
        "args": [
          "--directory",
          "/path/to/mcp-ctera-edge/src",
          "run",
          "stdio.py"
        ],
        "env": {
          "ctera.mcp.edge.settings.host": "",
          "ctera.mcp.edge.settings.user": "admin",
          "ctera.mcp.edge.settings.password": "your-password",
          "ctera.mcp.edge.settings.ssl": "true"
        }
      }
    }
  }
```

Configuration using SSE:

```bash
export ctera.mcp.edge.settings.host="your.ctera.edge.hostname.or.ipaddr"
export ctera.mcp.edge.settings.user="admin-username"
export ctera.mcp.edge.settings.password="admin-password"
export ctera.mcp.core.settings.ssl="true"
```

```powershell
$env:ctera.mcp.edge.settings.host = "your.ctera.edge.hostname.or.ipaddr"
$env:ctera.mcp.edge.settings.user = "admin-username"
$env:ctera.mcp.edge.settings.password = "admin-password"
$env:ctera.mcp.edge.settings.ssl = "true"
```

```json
{
  "mcpServers": {
    "ctera-edge-sse": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```
