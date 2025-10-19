# Dolibarr Tasks MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with secure access to Dolibarr task management functionality.

## Purpose

This MCP server provides a secure interface for AI assistants to interact with Dolibarr's Tasks API, enabling natural language interaction with your Dolibarr project tasks.

## Features

### Current Implementation

- **`dolibarr_get_task`** - Retrieve detailed information about a specific task by ID with optional time spent data
- **`dolibarr_create_task`** - Create a new task within a project with reference, label, and project ID
- **`dolibarr_modify_task`** - Update task information (label, description, progress, planned workload)
- **`dolibarr_task_add_spenttime`** - Add time spent entries to tasks with date, duration, and notes

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
# - dolibarr_tasks_server.py
# - README.md
# - CLAUDE.md
```

### Step 2: Build Docker Image

```bash
docker build -t dolibarr-tasks-mcp-server .
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

# Edit custom.yaml
vim ~/.docker/mcp/catalogs/custom.yaml
```

Add this entry to custom.yaml:

```yaml
version: 2
name: custom
displayName: Custom MCP Servers
registry:
  dolibarr_tasks:
    description: "Manage Dolibarr tasks via MCP - create, read, update tasks and manage time spent"
    title: "Dolibarr Tasks"
    type: server
    dateAdded: "2025-01-19T00:00:00Z"
    image: dolibarr-tasks-mcp-server:latest
    ref: ""
    readme: ""
    toolsUrl: ""
    source: ""
    upstream: ""
    icon: ""
    tools:
      - name: dolibarr_get_task
      - name: dolibarr_create_task
      - name: dolibarr_modify_task
      - name: dolibarr_task_add_spenttime
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
        - tasks
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
  dolibarr_tasks:
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
3. Your new Dolibarr Tasks tools should appear!

### Step 8: Test Your Server

```bash
# Verify it appears in the list
docker mcp server list

# If you don't see your server, check logs
docker logs [container_name]
```

## Usage Examples

In Claude Desktop, you can ask:

- "Show me the details of task ID 10"
- "Get task 5 with all time spent information"
- "Create a new task called 'Design mockups' for project 3 with reference TASK001"
- "Update task 7 to 75% progress"
- "Add 3.5 hours of work to task 12 for yesterday"
- "Log 2 hours on task 8 with note 'Initial development'"

## Architecture

```
Claude Desktop → MCP Gateway → Dolibarr Tasks MCP Server → Dolibarr API
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
python dolibarr_tasks_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python dolibarr_tasks_server.py
```

### Adding New Tools

1. Add the function to `dolibarr_tasks_server.py`
2. Decorate with `@mcp.tool()`
3. Follow the single-line docstring pattern
4. Update the catalog entry with the new tool name
5. Rebuild the Docker image

## Tool Reference

### dolibarr_get_task

Get complete task information including optional time spent data.

**Parameters:**
- `task_id` (required) - ID of the task
- `includetimespent` (optional) - 0=task only, 1=with summary, 2=with details (default: "0")

**Example:**
```
Get task 15 with detailed time spent
```

### dolibarr_create_task

Create a new task in a project.

**Parameters:**
- `ref` (required) - Task reference (e.g., "TASK001")
- `label` (required) - Task name/label
- `fk_project` (required) - Project ID
- `description` (optional) - Task description
- `planned_workload` (optional) - Planned hours (e.g., "8.5")
- `progress` (optional) - Progress percentage 0-100

**Example:**
```
Create a task "Design UI mockups" with reference TASK-DESIGN-001 in project 5 with 16 hours planned
```

### dolibarr_modify_task

Update an existing task.

**Parameters:**
- `task_id` (required) - ID of the task to update
- `label` (optional) - New task label
- `description` (optional) - New description
- `progress` (optional) - New progress percentage 0-100
- `planned_workload` (optional) - New planned hours

**Example:**
```
Update task 20 to 50% complete
```

### dolibarr_task_add_spenttime

Add a time spent entry to a task.

**Parameters:**
- `task_id` (required) - ID of the task
- `date` (required) - Date in format YYYY-MM-DD or YYYYMMDD
- `duration` (required) - Duration in hours (e.g., "2.5")
- `user_id` (optional) - User ID (defaults to current user)
- `note` (optional) - Note/description of work done

**Example:**
```
Add 3.5 hours to task 12 for 2025-01-18 with note "Bug fixing"
```

## Troubleshooting

### Tools Not Appearing

- Verify Docker image built successfully: `docker images | grep dolibarr-tasks`
- Check catalog and registry files are properly formatted
- Ensure Claude Desktop config includes custom catalog path
- Restart Claude Desktop completely

### Authentication Errors

- Verify secrets with `docker mcp secret ls`
- Ensure DOLIBARR_URL does not have trailing slash
- Verify API key is valid in your Dolibarr instance
- Check that API/Web Services module is enabled in Dolibarr

### API Errors

- Ensure your Dolibarr user has appropriate permissions (projet->lire, projet->creer, etc.)
- Check Dolibarr API logs for detailed error messages
- Verify the Dolibarr URL is accessible from your network

## Duration Format

Workload and time spent are specified in **hours** (decimal format):
- 30 minutes = 0.5
- 1 hour = 1
- 1.5 hours = 1.5
- 8 hours = 8

The server automatically converts hours to seconds for the API.

## Security Considerations

- All secrets stored in Docker Desktop secrets
- Never hardcode credentials in the code
- Server runs as non-root user (mcpuser)
- Sensitive data is never logged
- All API communication uses HTTPS (recommended)

## License

MIT License
