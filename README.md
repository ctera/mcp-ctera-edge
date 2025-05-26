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
          "/path/to/mcp-ctera-edge",
          "run",
          "src/stdio.py"
        ],
        "env": {
          "ctera.mcp.edge.settings.host": "your.ctera.edge.address",
          "ctera.mcp.edge.settings.user": "admin",
          "ctera.mcp.edge.settings.password": "your-password",
          "ctera.mcp.edge.settings.connector.ssl": false
        }
      }
    }
  }
```

Configuration using SSE:

```bash
export ctera.mcp.edge.settings.host="your.ctera.edge.ip"
export ctera.mcp.edge.settings.user="admin"
export ctera.mcp.edge.settings.password="your-password"
export ctera.mcp.edge.settings.connector.ssl="false"
```

```powershell
$env:ctera.mcp.edge.settings.host = "your.ctera.edge.ip"
$env:ctera.mcp.edge.settings.user = "admin"
$env:ctera.mcp.edge.settings.password = "your-password"
$env:ctera.mcp.edge.settings.connector.ssl = "false"
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

---

## 🛠️ Available Tools

- **ctera_edge_list_dir**: List directory contents with file metadata
- **ctera_edge_create_directory**: Create new directories
- **ctera_edge_copy_item**: Copy files and directories
- **ctera_edge_move_item**: Move files and directories
- **ctera_edge_delete_item**: Delete files and directories

---

## 🔐 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ctera.mcp.edge.settings.host` | CTERA Edge Filer IP/hostname | - | Yes |
| `ctera.mcp.edge.settings.user` | Username for authentication | - | Yes |
| `ctera.mcp.edge.settings.password` | Password for authentication | - | Yes |
| `ctera.mcp.edge.settings.connector.ssl` | Enable SSL connection | `true` | No |
| `ctera.mcp.edge.settings.port` | Connection port | `443` | No |
