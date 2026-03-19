# Error Codes & Troubleshooting Guide

Complete reference for error messages, codes, and solutions for the Dolibarr MCP Projects Server.

---

## Table of Contents

1. [HTTP Error Codes](#http-error-codes)
2. [Validation Errors](#validation-errors)
3. [Configuration Errors](#configuration-errors)
4. [Data Format Errors](#data-format-errors)
5. [Special Cases](#special-cases)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Debug Mode](#debug-mode)

---

## HTTP Error Codes

### 401 - Unauthorized

**Message:**
```
❌ Error: Authentication failed or insufficient permissions
```

**Possible Causes:**
1. Invalid API key
2. Expired API key
3. API key lacks required permissions
4. Web Services module not enabled in Dolibarr

**Solution:**

```bash
# 1. Verify API key is correct
echo $DOLIBARR_API_KEY

# 2. Test API key directly
curl -X GET "http://your-dolibarr/api/index.php/projects" \
  -H "DOLAPIKEY: your-api-key"

# 3. Check Dolibarr settings
# Go to: Setup → Modules → APIs → Web Services
# Ensure: Module is ENABLED

# 4. Verify user permissions
# Go to: Users → Select User → Permissions
# Ensure: User has "Read projects" permission
```

**Fix:**
- Generate new API key in Dolibarr user settings
- Update `DOLIBARR_API_KEY` environment variable
- Restart MCP gateway container

---

### 404 - Not Found

**Message (Project):**
```
❌ Error: Project {id} not found
```

**Message (Reference):**
```
❌ Error: Project with reference '{ref}' not found
```

**Possible Causes:**
1. Project ID doesn't exist
2. Project was deleted
3. Reference code is incorrect (typo)
4. Case sensitivity in reference search

**Solution:**

```bash
# 1. List all projects to verify
dolibarr_list_projects()

# 2. Check project exists in Dolibarr
# Login to Dolibarr → Projects/Leads → List

# 3. For reference search, verify exact spelling
dolibarr_get_project_by_ref(ref="PJ2512-0001")  # ✅ Correct
dolibarr_get_project_by_ref(ref="pj2512-0001")  # ❌ Case sensitive
```

**Fix:**
- Verify project ID/reference is correct
- Use `dolibarr_list_projects()` to find correct ID/reference
- Check for typos in reference codes

---

### 400 - Bad Request

**Message:**
```
❌ Error: Invalid request - {details}
```

**Possible Causes:**
1. Malformed JSON in request body
2. Invalid parameter types
3. Duplicate project reference
4. Required fields missing

**Solution:**

```bash
# 1. Check for duplicate reference
# Error: "Reference already exists"
# Solution: Use unique reference code

# 2. Verify all required fields
dolibarr_create_project(
    ref="UNIQUE-REF",     # ✅ Required
    title="Project Title" # ✅ Required
)

# 3. Check parameter types
dolibarr_create_project(
    ref="PJ-001",
    title="Test",
    fk_soc="not-a-number"  # ❌ Error: must be integer
)
```

**Fix:**
- Use unique project references
- Provide all required fields
- Ensure correct data types

---

### 500 - Internal Server Error

**Message:**
```
❌ API Error: 500 - {error details}
```

**Possible Causes:**
1. Dolibarr database issue
2. Dolibarr module misconfiguration
3. PHP error in Dolibarr
4. Database constraint violation

**Solution:**

```bash
# 1. Check Dolibarr logs
docker logs dolibarr-container

# 2. Check database connection
docker exec dolibarr-db mysql -u user -p -e "SELECT 1"

# 3. Verify Dolibarr is running
curl http://your-dolibarr/
```

**Fix:**
- Check Dolibarr error logs
- Verify database is running and accessible
- Restart Dolibarr container if needed
- Contact Dolibarr administrator

---

## Validation Errors

### Missing Required Field: ref

**Message:**
```
❌ Error: ref (project reference) is required
```

**Cause:** `ref` parameter is empty or not provided

**Solution:**
```python
# ❌ Wrong
dolibarr_create_project(title="Test")

# ✅ Correct
dolibarr_create_project(ref="PJ2512-0001", title="Test")
```

---

### Missing Required Field: title

**Message:**
```
❌ Error: title is required
```

**Cause:** `title` parameter is empty or not provided

**Solution:**
```python
# ❌ Wrong
dolibarr_create_project(ref="PJ2512-0001")

# ✅ Correct
dolibarr_create_project(ref="PJ2512-0001", title="Project Title")
```

---

### Missing Required Field: project_id

**Message:**
```
❌ Error: project_id is required and must be a positive integer
```

**Cause:** Project ID is 0, negative, or not provided

**Solution:**
```python
# ❌ Wrong
dolibarr_get_project(project_id=0)
dolibarr_get_project(project_id=-1)

# ✅ Correct
dolibarr_get_project(project_id=1)
```

---

## Data Format Errors

### Invalid Integer: fk_soc

**Message:**
```
❌ Error: fk_soc must be a valid integer, got: {value}
```

**Cause:** Third party ID is not a valid integer

**Solution:**
```python
# ❌ Wrong
dolibarr_create_project(
    ref="PJ-001",
    title="Test",
    fk_soc="ABC"          # Not a number
)

# ✅ Correct
dolibarr_create_project(
    ref="PJ-001",
    title="Test",
    fk_soc="1"            # Valid integer as string
)
```

**Note:** Parameter accepts string but converts to integer internally

---

### Invalid Float: budget_amount

**Message:**
```
❌ Error: budget_amount must be a valid number, got: {value}
```

**Cause:** Budget amount is not a valid number

**Solution:**
```python
# ❌ Wrong
dolibarr_create_project(
    ref="PJ-001",
    title="Test",
    budget_amount="ABC"       # Not a number
)

# ✅ Correct
dolibarr_create_project(
    ref="PJ-001",
    title="Test",
    budget_amount="50000.50"  # Valid number
)
```

---

### Invalid Number Format

**Message:**
```
❌ Error: Invalid number format - {details}
```

**Cause:** Pagination parameters (limit, page) are not valid integers

**Solution:**
```python
# ❌ Wrong
dolibarr_list_projects(limit="ABC", page="XYZ")

# ✅ Correct
dolibarr_list_projects(limit="100", page="0")
```

---

## Configuration Errors

### Missing DOLIBARR_URL

**Message:**
```
❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured
```

**Cause:** `DOLIBARR_URL` environment variable not set

**Solution:**

```bash
# 1. Check environment variables
docker exec mcp-gateway env | grep DOLIBARR

# 2. Set in docker-compose.yml or .env
DOLIBARR_URL=http://your-dolibarr/htdocs    # e.g. http://my-server/htdocs
DOLIBARR_API_KEY=your-api-key-here

# 3. Restart containers
docker restart mcp_dolibarr
```

**Fix:**
- Set `DOLIBARR_URL` environment variable
- Format: `http://hostname/htdocs` (no trailing slash)
- Restart MCP gateway after changes

---

### Missing DOLIBARR_API_KEY

**Message:**
```
❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured
```

**Cause:** `DOLIBARR_API_KEY` environment variable not set

**Solution:**

```bash
# 1. Generate API key in Dolibarr
# Login → User Settings → Security → API Key → Generate

# 2. Set environment variable
DOLIBARR_API_KEY=your-api-key-here

# 3. Restart gateway
docker restart mcp_dolibarr
```

---

## Special Cases

### No Projects Found

**Message:**
```
📊 No projects found
```

**Cause:**
- No projects exist in the system
- No projects match the filter criteria
- Pagination page is beyond available data

**Solution:**
```python
# 1. Check if any projects exist
dolibarr_list_all_projects()

# 2. Verify pagination parameters
dolibarr_list_projects(page="0")  # Start at first page

# 3. Create a test project
dolibarr_create_project(ref="TEST-001", title="Test Project")
```

**Note:** This is not an error - informational message only

---

### No Tasks Found

**Message:**
```
📊 No tasks found for project {id}
```

**Cause:** Project exists but has no tasks assigned

**Solution:**
```python
# 1. Verify project exists
dolibarr_get_project(project_id=1)

# 2. Create tasks in Dolibarr
# Login → Projects → Select Project → Tasks → Add Task
```

**Note:** This is not an error - informational message only

---

### Deletion Warning (v1.1.0+)

**Message:**
```
⚠️ Warning: This will permanently delete project {id}.
This action is irreversible and will remove all project data.

To confirm deletion, call this tool again with: confirm='yes'
```

**Cause:** Deletion called without confirmation parameter

**Solution:**
```python
# First call (returns warning)
dolibarr_delete_project(project_id=13)

# Second call (confirms deletion)
dolibarr_delete_project(project_id=13, confirm="yes")
```

**Note:** This is a safety feature introduced in v1.1.0

---

### Missing Update Fields

**Message:**
```
❌ Error: At least one field to update must be provided (title, description, or budget_amount)
```

**Cause:** Update called with no fields specified

**Solution:**
```python
# ❌ Wrong
dolibarr_update_project(project_id=1)

# ✅ Correct - provide at least one field
dolibarr_update_project(
    project_id=1,
    title="New Title"
)
```

---

### Invalid Time Spent Parameter

**Message:**
```
❌ Error: includetimespent must be 0, 1, or 2
```

**Cause:** Invalid value for `includetimespent` parameter

**Solution:**
```python
# ❌ Wrong
dolibarr_get_project_tasks(project_id=1, includetimespent=5)

# ✅ Correct
dolibarr_get_project_tasks(project_id=1, includetimespent=0)  # No time data
dolibarr_get_project_tasks(project_id=1, includetimespent=1)  # Basic time
dolibarr_get_project_tasks(project_id=1, includetimespent=2)  # Detailed time
```

---

## Troubleshooting Guide

### Issue: Third Party ID Not Displaying

**Symptom:** Project created with `fk_soc` but Third Party ID not shown

**Versions Affected:** v1.0.0 only

**Solution:**
```bash
# Upgrade to v1.1.0+
# Bug was fixed in version 1.1.0

# Verify version
docker images | grep dolibarr-projects

# If using v1.0.0, rebuild
cd mcp-gateway-standalone
docker compose build --no-cache dolibarr-projects
docker restart mcp_dolibarr
```

**Root Cause:** Bug in v1.0.0 - only checked `fk_soc` field but API returns `socid`

---

### Issue: Project Not Associated with Third Party

**Symptom:** Created project with `fk_soc` but `socid` is NULL in database

**Versions Affected:** v1.0.0 only

**Solution:**
```bash
# 1. Upgrade to v1.1.0+ (bug fixed)
cd mcp-gateway-standalone
docker compose build --no-cache dolibarr-projects
docker restart mcp_dolibarr

# 2. Recreate affected projects
dolibarr_create_project(
    ref="NEW-REF",
    title="New Project",
    fk_soc="1"  # Now works correctly
)
```

**Root Cause:** Bug in v1.0.0 - sent field as `fk_soc` but API expects `socid`

---

### Issue: Connection Timeout

**Symptom:**
```
❌ Error: timeout
```

**Possible Causes:**
1. Dolibarr server is down
2. Network connectivity issue
3. Firewall blocking connection
4. Very large dataset (list_all_projects)

**Solution:**

```bash
# 1. Test Dolibarr connectivity
curl http://your-dolibarr/

# 2. Check network from container
docker exec mcp_dolibarr ping your-dolibarr-host

# 3. Verify Dolibarr is in same network
docker network inspect lamp_default

# 4. For large datasets, use pagination instead
dolibarr_list_projects(limit="100", page="0")  # Instead of list_all
```

---

### Issue: Gateway Panic / Server Crash

**Symptom:** MCP gateway crashes or panics

**Possible Causes:**
1. Multi-line docstrings in code (violates MCP constraints)
2. Invalid type hints
3. Memory issue

**Solution:**

```bash
# 1. Check gateway logs
docker logs mcp_dolibarr

# 2. Look for panic messages
# Common: "panic: docstring too long"

# 3. Verify code follows MCP constraints (see CLAUDE.md)
# - Single-line docstrings only
# - No typing module imports
# - Simple parameter types

# 4. Rebuild with latest code
cd mcp-gateway-standalone
docker compose build --no-cache dolibarr-projects
docker restart mcp_dolibarr
```

---

### Issue: Tools Not Appearing in Agent

**Symptom:** MCP tools don't show up in AI agent interface

**Solution:**

```bash
# 1. Verify server is running
docker ps | grep dolibarr

# 2. Check gateway logs
docker logs mcp_dolibarr

# 3. Verify catalog configuration
cat ~/.docker/mcp/catalogs/custom.yaml

# 4. Rebuild and restart
cd mcp-gateway-standalone
docker compose build --no-cache dolibarr-projects
docker restart mcp_dolibarr

# 5. Wait for gateway to initialize
sleep 10

# 6. Test with curl
curl -X POST http://localhost:5678/webhook/webhook_message \
  -H "Content-Type: application/json" \
  -d '{"message": "List all projects"}'
```

---

## Debug Mode

### Enable Debug Logging

**Location:** `mcp-server-projects/dolibarr_projects_server.py`

```python
# Current level
logging.basicConfig(
    level=logging.INFO,
    ...
)

# Change to DEBUG for detailed logs
logging.basicConfig(
    level=logging.DEBUG,
    ...
)
```

**Rebuild after change:**
```bash
docker compose build --no-cache dolibarr-projects
docker compose build --no-cache dolibarr-projects
docker restart mcp_dolibarr
```

---

### View Logs

**Gateway Logs:**
```bash
# Real-time
docker logs -f mcp_dolibarr

# Last 100 lines
docker logs --tail 100 mcp_dolibarr
```

**MCP Server Logs:**
```bash
# Logs go to gateway stderr
docker logs mcp_dolibarr 2>&1 | grep "dolibarr-projects"
```

---

### Test API Directly

**Bypass MCP and test Dolibarr API:**

```bash
# List projects
curl -X GET "http://your-dolibarr/htdocs/api/index.php/projects" \
  -H "DOLAPIKEY: your-api-key-here"

# Get project by ID
curl -X GET "http://your-dolibarr/htdocs/api/index.php/projects/1" \
  -H "DOLAPIKEY: your-api-key-here"

# Create project
curl -X POST "http://your-dolibarr/htdocs/api/index.php/projects" \
  -H "DOLAPIKEY: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"ref": "TEST-API", "title": "Test", "socid": 1}'
```

---

## Error Summary Table

| Error Code | Category | Severity | User Action Required |
|------------|----------|----------|---------------------|
| 401 | Authentication | 🔴 High | Fix API key |
| 404 | Not Found | 🟡 Medium | Verify ID/reference |
| 400 | Bad Request | 🟡 Medium | Fix parameters |
| 500 | Server Error | 🔴 High | Contact admin |
| Missing ref | Validation | 🟡 Medium | Provide ref |
| Missing title | Validation | 🟡 Medium | Provide title |
| Invalid fk_soc | Validation | 🟢 Low | Fix data type |
| Invalid budget | Validation | 🟢 Low | Fix data type |
| Config missing | Configuration | 🔴 High | Set env vars |
| No projects | Information | ⚪ Info | None |
| Deletion warning | Safety | 🟡 Medium | Confirm deletion |

---

## Getting Help

**Check Documentation:**
1. CHANGELOG.md - Recent changes and fixes
2. API_MAPPING.md - API endpoint details
3. CLAUDE.md - Development guidelines

**Report Issues:**
- Include error message
- Include MCP tool call that failed
- Include version number
- Include relevant logs

**Common Solutions:**
- Restart gateway: `docker restart mcp_dolibarr`
- Rebuild server: `docker compose build --no-cache dolibarr-projects`
- Rebuild server: `docker compose build --no-cache dolibarr_tasks`
- Check logs: `docker logs mcp_dolibarr`
- Verify config: Check environment variables

---

*Last Updated: 2025-12-18*
*Version: 1.1.0*
