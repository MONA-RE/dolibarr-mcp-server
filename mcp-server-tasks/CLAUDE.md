# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server for Dolibarr task management. It exposes Dolibarr's Tasks API via the MCP protocol, allowing AI assistants to interact with Dolibarr tasks naturally.

## Architecture

### Tech Stack
- **Python 3.11**: Core language
- **FastMCP**: MCP server framework
- **httpx**: Async HTTP client for Dolibarr API calls
- **Docker**: Container runtime

### Key Components

1. **dolibarr_tasks_server.py**: Main server implementation
   - Implements 4 MCP tools for task management
   - Uses async/await for all API calls
   - Follows strict MCP server patterns (no prompts, single-line docstrings)

2. **Dockerfile**: Container definition
   - Python 3.11-slim base
   - Non-root user (mcpuser)
   - Optimized layer caching

3. **requirements.txt**: Python dependencies
   - mcp[cli]>=1.2.0
   - httpx

## MCP Server Constraints

### CRITICAL RULES (DO NOT VIOLATE)

1. **NO `@mcp.prompt()` decorators** - Breaks Claude Desktop
2. **NO `prompt` parameter to FastMCP()** - Breaks Claude Desktop
3. **NO type hints from typing module** - No `Optional`, `Union`, `List[str]`
4. **NO complex parameter types** - Use `param: str = ""` not `param: str = None`
5. **SINGLE-LINE DOCSTRINGS ONLY** - Multi-line docstrings cause gateway panic
6. **DEFAULT TO EMPTY STRINGS** - Use `param: str = ""` never `param: str = None`
7. **ALWAYS return strings from tools** - All tools must return formatted strings
8. **ALWAYS log to stderr** - Use the logging configuration provided

### Tool Implementation Pattern

```python
@mcp.tool()
async def tool_name(param: str = "") -> str:
    """Single-line description of what this tool does - MUST BE ONE LINE."""
    logger.info(f"Executing tool_name with {param}")

    try:
        # Implementation here
        result = "example"
        return f"✅ Success: {result}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {str(e)}"
```

## Dolibarr API Integration

### Authentication
- Uses `DOLAPIKEY` header with API key
- API key stored in Docker secrets as `DOLIBARR_API_KEY`
- Base URL stored as `DOLIBARR_URL`

### API Endpoints Used

All endpoints are relative to `{DOLIBARR_URL}/api/index.php`:

- `GET /tasks/{id}` - Get task details with optional time spent
- `GET /tasks` - List tasks (supports pagination, sorting, filtering)
- `POST /tasks` - Create task
- `PUT /tasks/{id}` - Update task
- `POST /tasks/{id}/addtimespent` - Add time spent entry

### Error Handling

- 401: Authentication failed or insufficient permissions
- 404: Resource not found
- 400: Bad request (missing required fields)
- 500: Server error

## Development Workflow

### Testing Locally

```bash
# Set environment variables
export DOLIBARR_URL="https://your-dolibarr.com"
export DOLIBARR_API_KEY="your_api_key"

# Run server
python dolibarr_tasks_server.py
```

### Building Docker Image

```bash
docker build -t dolibarr-tasks-mcp-server .
```

### Adding New Tools

1. Add async function to `dolibarr_tasks_server.py`
2. Decorate with `@mcp.tool()`
3. Follow the tool implementation pattern above
4. Update `custom.yaml` catalog with new tool name
5. Rebuild Docker image
6. Restart Claude Desktop

## Configuration Files

### custom.yaml (MCP Catalog)
Located at `~/.docker/mcp/catalogs/custom.yaml`
- Defines server metadata
- Lists available tools
- Specifies required secrets

### registry.yaml (MCP Registry)
Located at `~/.docker/mcp/registry.yaml`
- Registers the server with MCP gateway
- Must include `dolibarr_tasks: {ref: ""}`

### claude_desktop_config.json
- Configures Claude Desktop to use MCP gateway
- Must include `--catalog=/mcp/catalogs/custom.yaml` argument

## Common Issues

### Gateway Panic Errors
- Usually caused by multi-line docstrings
- Check all `@mcp.tool()` functions have single-line docstrings

### Tools Not Appearing
- Verify Docker image built successfully
- Check custom.yaml is properly formatted (YAML is whitespace-sensitive)
- Ensure Claude Desktop config includes custom catalog path
- Restart Claude Desktop completely

### Authentication Errors
- Verify `DOLIBARR_URL` has no trailing slash
- Check API key is valid in Dolibarr
- Ensure API/Web Services module is enabled in Dolibarr
- Verify user has appropriate permissions

## Code Style

### Logging
- Log to stderr only
- Use logger.info() for operations
- Use logger.error() for errors with exc_info=True for exceptions

### Error Messages
- Use emoji prefixes: ✅ for success, ❌ for errors, 📊 for data, ⏱️ for time
- Return user-friendly error messages
- Include context in error messages

### Parameter Validation
- Always check for empty strings with `.strip()`
- Convert string parameters to appropriate types (int, float) with try/except
- Validate all required parameters before making API calls

### Duration Conversion
- Input: Hours (decimal, e.g., "2.5" = 2h30m)
- Storage: Seconds (integer, e.g., 9000)
- Conversion: `seconds = int(hours * 3600)`
- Display: `hours = seconds / 3600`

## Tools Reference

### dolibarr_get_task
**Purpose**: Retrieve detailed task information with optional time spent data

**Parameters**:
- `task_id` (required): Task ID
- `includetimespent` (optional): 0=task only, 1=summary, 2=detailed lines

**API**: `GET /tasks/{id}?includetimespent={0|1|2}`

**Permission**: `projet->lire`

### dolibarr_create_task
**Purpose**: Create a new task in a project

**Parameters**:
- `ref` (required): Task reference code
- `label` (required): Task name/title
- `fk_project` (required): Project ID
- `description` (optional): Task description
- `planned_workload` (optional): Planned hours (converted to seconds)
- `progress` (optional): Progress percentage (0-100)

**API**: `POST /tasks`

**Permission**: `projet->creer`

### dolibarr_modify_task
**Purpose**: Update existing task information

**Parameters**:
- `task_id` (required): Task ID to update
- `label` (optional): New task label
- `description` (optional): New description
- `progress` (optional): New progress percentage (0-100)
- `planned_workload` (optional): New planned hours

**API**: `PUT /tasks/{id}`

**Permission**: `projet->creer`

**Note**: Does NOT update time spent data

### dolibarr_task_add_spenttime
**Purpose**: Add a time spent entry to a task

**Parameters**:
- `task_id` (required): Task ID
- `date` (required): Date (YYYY-MM-DD or YYYYMMDD)
- `duration` (required): Duration in hours (e.g., "2.5")
- `user_id` (optional): User ID (defaults to current user)
- `note` (optional): Work description/notes

**API**: `POST /tasks/{id}/addtimespent`

**Permission**: `projet->creer`

## Security

- Never log API keys or sensitive data
- All secrets in Docker Desktop secrets
- Run as non-root user in container
- Use HTTPS for Dolibarr API (recommended)
- Validate and sanitize all inputs

## Future Enhancements

Potential additional tools:
- dolibarr_delete_task (DELETE /tasks/{id})
- dolibarr_list_tasks (GET /tasks with filters)
- dolibarr_get_task_roles (GET /tasks/{id}/roles)
- dolibarr_validate_task (if validation endpoint exists)
- dolibarr_list_task_timespent (dedicated time spent listing)

When adding these, follow the same patterns and constraints as existing tools.

## Time/Duration Helper

### JavaScript
```javascript
function hoursToSeconds(hours) {
  return Math.floor(hours * 3600);
}

function secondsToHours(seconds) {
  return (seconds / 3600).toFixed(2);
}
```

### Python
```python
def hours_to_seconds(hours: float) -> int:
    return int(hours * 3600)

def seconds_to_hours(seconds: int) -> float:
    return round(seconds / 3600, 2)
```

### Conversion Table
| Hours | Minutes | Seconds |
|-------|---------|---------|
| 0.25  | 15      | 900     |
| 0.5   | 30      | 1800    |
| 1     | 60      | 3600    |
| 2     | 120     | 7200    |
| 4     | 240     | 14400   |
| 8     | 480     | 28800   |

## Related Documentation

- [Dolibarr Tasks API Documentation](../Dolibarr_api_documentation/tasks.md)
- [Dolibarr Projects MCP Server](../mcp-server/README.md)
- [Tasks API Fields Reference](../Dolibarr_api_documentation/tasks/api_fields_task.md)
