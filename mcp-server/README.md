# Dolibarr Projects MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with secure access to Dolibarr project management functionality.

## Purpose

This MCP server provides a secure interface for AI assistants to interact with Dolibarr's project management API, enabling natural language interaction with your Dolibarr projects.

## Features

### Current Implementation

- **`dolibarr_get_project`** - Retrieve detailed information about a specific project by ID
- **`dolibarr_list_projects`** - List all projects with pagination and sorting options
- **`dolibarr_create_project`** - Create a new project with reference, title, and optional details
- **`dolibarr_update_project`** - Update project information (title, description, budget)
- **`dolibarr_delete_project`** - Delete a project by ID
- **`dolibarr_get_project_tasks`** - Retrieve all tasks associated with a project

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command available)
- A running Dolibarr instance with API/Web Services module enabled
- Dolibarr API key generated from your user profile

## Installation

### Step 1: Save the Files

```bash
# All files should be in the same directory:
# - Dockerfile
# - requirements.txt
# - dolibarr_projects_server.py
# - README.txt
# - CLAUDE.md
```

### Step 2: Build Docker Image

```bash
docker build -t dolibarr-projects-mcp-server .
```

### Step 3: Set Up Secrets

```bash
# Set your Dolibarr URL
docker mcp secret set DOLIBARR_URL="https://your-dolibarr-instance.com"

# Set your Dolibarr API key
docker mcp secret set DOLIBARR_API_KEY="your_api_key_here"

# Verify secrets are set
docker mcp secret ls
```

### Step 4: Create Custom Catalog

```bash
# Create catalogs directory if it doesn't exist
mkdir -p ~/.docker/mcp/catalogs

# Create or edit dolibarr-custom.yaml
vim ~/.docker/mcp/catalogs/dolibarr-custom.yaml
```

Add this entry to custom.yaml:

```yaml
version: 2
name: custom
displayName: Custom MCP Servers
registry:
  dolibarr_projects:
    description: "Manage Dolibarr projects via MCP - create, read, update, delete projects and tasks"
    title: "Dolibarr Projects"
    type: server
    dateAdded: "2025-10-18T00:00:00Z"
    image: dolibarr-projects-mcp-server:latest
    ref: ""
    readme: ""
    toolsUrl: ""
    source: ""
    upstream: ""
    icon: ""
    tools:
      - name: dolibarr_get_project
      - name: dolibarr_list_projects
      - name: dolibarr_create_project
      - name: dolibarr_update_project
      - name: dolibarr_delete_project
      - name: dolibarr_get_project_tasks
    secrets:
      - name: DOLIBARR_URL
        env: DOLIBARR_URL
        example: https://your-dolibarr.com
      - name: DOLIBARR_API_KEY
        env: DOLIBARR_API_KEY
        example: your_api_key_here
    metadata:
      category: integration
      tags:
        - dolibarr
        - project-management
        - erp
        - crm
      license: MIT
      owner: teddy.morel@mona.re
```

### Step 5: Update Registry

```bash
# Edit registry file
vim ~/.docker/mcp/registry.yaml
```

Add this entry under the existing `registry:` key:

```yaml
registry:
  # ... existing servers ...
  dolibarr_projects:
    ref: ""
```

**IMPORTANT**: The entry must be under the `registry:` key, not at the root level.

### Step 6: Configure Claude Desktop

Find your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Edit the file and add your custom catalog to the args array:

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "-v", "[YOUR_HOME]/.docker/mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/custom.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

Replace `[YOUR_HOME]` with:
- **macOS**: `/Users/your_username`
- **Windows**: `C:\\Users\\your_username` (use double backslashes)
- **Linux**: `/home/your_username`

### Step 7: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Start Claude Desktop again
3. Your new Dolibarr tools should appear!

### Step 8: Test Your Server

```bash
# Verify it appears in the list
docker mcp server list

# If you don't see your server, check logs
docker logs [container_name]
```

## Usage Examples

In Claude Desktop, you can ask:

- "List all my Dolibarr projects"
- "Show me details for project ID 5"
- "Create a new project called 'Website Redesign' with reference PROJ2024-001"
- "Update project 3 to have a budget of 50000"
- "Show me all tasks for project 7"
- "Delete project 12"

## Architecture

```
Claude Desktop → MCP Gateway → Dolibarr Projects MCP Server → Dolibarr API
                                       ↓
                             Docker Desktop Secrets
                          (DOLIBARR_URL, DOLIBARR_API_KEY)
```

## Development

### Local Testing

```bash
# Set environment variables for testing
export DOLIBARR_URL="https://your-dolibarr-instance.com"
export DOLIBARR_API_KEY="your_api_key_here"

# Run directly
python dolibarr_projects_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python dolibarr_projects_server.py
```

### Adding New Tools

1. Add the function to `dolibarr_projects_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Troubleshooting

### Tools Not Appearing

- Verify Docker image built successfully: `docker images | grep dolibarr-projects`
- Check catalog and registry files are properly formatted
- Ensure Claude Desktop config includes custom catalog path
- Restart Claude Desktop completely

### Authentication Errors

- Verify secrets with `docker mcp secret list`
- Ensure DOLIBARR_URL does not have trailing slash
- Verify API key is valid in your Dolibarr instance
- Check that API/Web Services module is enabled in Dolibarr

### API Errors

- Ensure your Dolibarr user has appropriate permissions (projet->lire, projet->creer, etc.)
- Check Dolibarr API logs for detailed error messages
- Verify the Dolibarr URL is accessible from your network

## Security Considerations

- All secrets stored in Docker Desktop secrets
- Never hardcode credentials in the code
- Server runs as non-root user (mcpuser)
- Sensitive data is never logged
- All API communication uses HTTPS (recommended)

## Acknowledgments

This MCP server was built using the guide and template from [theNetworkChuck's Docker MCP Tutorial](https://github.com/theNetworkChuck/docker-mcp-tutorial/blob/main/README.md).

Special thanks to **NetworkChuck** for creating an excellent tutorial and template that made building this MCP server possible!

## License

MIT License
