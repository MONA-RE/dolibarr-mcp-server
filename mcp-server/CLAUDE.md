# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server for Dolibarr project management. It exposes Dolibarr's Projects API via the MCP protocol, allowing AI assistants to interact with Dolibarr projects naturally.

## Architecture

### Tech Stack
- **Python 3.11**: Core language
- **FastMCP**: MCP server framework
- **httpx**: Async HTTP client for Dolibarr API calls
- **Docker**: Container runtime

### Key Components

1. **dolibarr_projects_server.py**: Main server implementation
   - Implements 6 MCP tools for project management
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
    """Single-line description of what this tool does."""
    logger.info(f"Executing tool_name with {param}")

    if not param.strip():
        return "❌ Error: param is required"

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

- `GET /projects/{id}` - Get project details
- `GET /projects` - List projects (supports pagination, sorting, filtering)
- `POST /projects` - Create project
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project
- `GET /projects/{id}/tasks` - Get project tasks

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
python dolibarr_projects_server.py
```

### Building Docker Image

```bash
docker build -t dolibarr-projects-mcp-server .
```

### Adding New Tools

1. Add async function to `dolibarr_projects_server.py`
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
- Must include `dolibarr_projects: {ref: ""}`

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
- Use emoji prefixes: ✅ for success, ❌ for errors, 📊 for data
- Return user-friendly error messages
- Include context in error messages

### Parameter Validation
- Always check for empty strings with `.strip()`
- Convert string parameters to appropriate types (int, float) with try/except
- Validate all required parameters before making API calls

## Security

- Never log API keys or sensitive data
- All secrets in Docker Desktop secrets
- Run as non-root user in container
- Use HTTPS for Dolibarr API (recommended)
- Validate and sanitize all inputs

## Future Enhancements

Potential additional tools:
- validate_project (POST /projects/{id}/validate)
- get_project_roles (GET /projects/{id}/roles)
- filter_projects_by_category (using category parameter)
- filter_projects_by_thirdparty (using thirdparty_ids parameter)
- advanced_filter_projects (using sqlfilters parameter)

When adding these, follow the same patterns and constraints as existing tools.
