# API Mapping - MCP Tools ↔ Dolibarr API

This document provides a complete mapping between MCP server tools and Dolibarr REST API endpoints, including field name conversions and important notes.

---

## Table of Contents

1. [Overview](#overview)
2. [Read Operations](#read-operations)
3. [Write Operations](#write-operations)
4. [Field Mappings](#field-mappings)
5. [Status Codes](#status-codes)
6. [Examples](#examples)

---

## Overview

**Base URL Pattern:**
```
{DOLIBARR_URL}/api/index.php/projects
```

**Authentication:**
- Header: `DOLAPIKEY: {API_KEY}`
- Method: API Key authentication

**Response Format:** JSON

---

## Read Operations

### 1. Get Project by ID

| Property | Value |
|----------|-------|
| **MCP Tool** | `dolibarr_get_project(project_id: int)` |
| **HTTP Method** | GET |
| **Endpoint** | `/api/index.php/projects/{id}` |
| **Parameters** | `project_id` (int, required) |
| **Response** | Single project object |
| **Timeout** | 10 seconds |

**Example:**
```python
# MCP Call
dolibarr_get_project(project_id=1)

# API Call
GET /api/index.php/projects/1
Headers: DOLAPIKEY: xxx
```

---

### 2. Get Project by Reference

| Property | Value |
|----------|-------|
| **MCP Tool** | `dolibarr_get_project_by_ref(ref: str)` |
| **HTTP Method** | GET |
| **Endpoint** | `/api/index.php/projects` |
| **Parameters** | `sqlfilters=(t.ref:=:'REFERENCE')` |
| **Response** | Array of projects (first element used) |
| **Timeout** | 10 seconds |
| **Version** | Added in v1.1.0 |

**Example:**
```python
# MCP Call
dolibarr_get_project_by_ref(ref="PJ2512-0001")

# API Call
GET /api/index.php/projects?sqlfilters=(t.ref:=:'PJ2512-0001')
Headers: DOLAPIKEY: xxx
```

---

### 3. List Projects (Paginated)

| Property | Value |
|----------|-------|
| **MCP Tool** | `dolibarr_list_projects(limit, page, sortfield, sortorder)` |
| **HTTP Method** | GET |
| **Endpoint** | `/api/index.php/projects` |
| **Parameters** | See table below |
| **Response** | Array of project objects |
| **Timeout** | 10 seconds |

**Parameters:**

| MCP Parameter | API Parameter | Type | Default | Description |
|---------------|---------------|------|---------|-------------|
| `limit` | `limit` | string → int | "100" | Number of projects per page |
| `page` | `page` | string → int | "0" | Page number (0-indexed) |
| `sortfield` | `sortfield` | string | "t.rowid" | Field to sort by |
| `sortorder` | `sortorder` | string | "ASC" | Sort order (ASC/DESC) |

**Example:**
```python
# MCP Call
dolibarr_list_projects(limit="50", page="0", sortfield="t.ref", sortorder="ASC")

# API Call
GET /api/index.php/projects?limit=50&page=0&sortfield=t.ref&sortorder=ASC
Headers: DOLAPIKEY: xxx
```

---

### 4. List All Projects (Auto-Pagination)

| Property | Value |
|----------|-------|
| **MCP Tool** | `dolibarr_list_all_projects(sortfield, sortorder)` |
| **HTTP Method** | GET (multiple calls) |
| **Endpoint** | `/api/index.php/projects` |
| **Parameters** | `sortfield`, `sortorder` |
| **Response** | Combined array of all projects |
| **Timeout** | 30 seconds per page |
| **Version** | Added in v1.1.0 |

**Internal Behavior:**
- Fetches 100 projects per page
- Continues until receiving less than 100 projects
- Combines all results into single response

**Example:**
```python
# MCP Call
dolibarr_list_all_projects(sortfield="t.ref", sortorder="ASC")

# Internal API Calls (automatic)
GET /api/index.php/projects?limit=100&page=0&sortfield=t.ref&sortorder=ASC
GET /api/index.php/projects?limit=100&page=1&sortfield=t.ref&sortorder=ASC
# ... continues until less than 100 results
```

---

### 5. Get Project Tasks

| Property | Value |
|----------|-------|
| **MCP Tool** | `dolibarr_get_project_tasks(project_id, includetimespent)` |
| **HTTP Method** | GET |
| **Endpoint** | `/api/index.php/projects/{id}/tasks` |
| **Parameters** | See table below |
| **Response** | Array of task objects |
| **Timeout** | 10 seconds |

**Parameters:**

| MCP Parameter | API Parameter | Type | Default | Description |
|---------------|---------------|------|---------|-------------|
| `project_id` | Path parameter | int | (required) | Project ID |
| `includetimespent` | `includetimespent` | int | 0 | Include time tracking (0=no, 1=yes, 2=detailed) |

**Example:**
```python
# MCP Call
dolibarr_get_project_tasks(project_id=1, includetimespent=1)

# API Call
GET /api/index.php/projects/1/tasks?includetimespent=1
Headers: DOLAPIKEY: xxx
```

---

## Write Operations

### 6. Create Project

| Property | Value |
|----------|-------|
| **MCP Tool** | `dolibarr_create_project(ref, title, description, fk_soc, budget_amount)` |
| **HTTP Method** | POST |
| **Endpoint** | `/api/index.php/projects` |
| **Body** | JSON object (see field mapping) |
| **Response** | New project ID (integer) |
| **Timeout** | 10 seconds |

**Field Mapping (IMPORTANT):**

| MCP Parameter | API Field Name | Type | Required | Notes |
|---------------|----------------|------|----------|-------|
| `ref` | `ref` | string | ✅ Yes | Project reference code |
| `title` | `title` | string | ✅ Yes | Project title |
| `description` | `description` | string | ❌ No | Project description |
| `fk_soc` | **`socid`** | integer | ❌ No | ⚠️ **Field name changed in v1.1.0** |
| `budget_amount` | `budget_amount` | float | ❌ No | Project budget |

**⚠️ CRITICAL NOTE:**
- MCP parameter is named `fk_soc` (for consistency with Dolibarr database schema)
- But it's sent to API as **`socid`** (API requirement)
- **Bug fixed in v1.1.0** - Previously sent as `fk_soc` which was ignored by API

**Example:**
```python
# MCP Call
dolibarr_create_project(
    ref="PJ2512-0010",
    title="New Project",
    description="Project description",
    fk_soc="1",
    budget_amount="50000.00"
)

# API Call
POST /api/index.php/projects
Headers:
  DOLAPIKEY: xxx
  Content-Type: application/json
Body:
{
    "ref": "PJ2512-0010",
    "title": "New Project",
    "description": "Project description",
    "socid": 1,                    ← Note: socid, not fk_soc
    "budget_amount": 50000.00
}

# Response
13  (new project ID)
```

---

### 7. Update Project

| Property | Value |
|----------|-------|
| **MCP Tool** | `dolibarr_update_project(project_id, title, description, budget_amount)` |
| **HTTP Method** | PUT |
| **Endpoint** | `/api/index.php/projects/{id}` |
| **Body** | JSON object with fields to update |
| **Response** | Updated project object |
| **Timeout** | 10 seconds |

**Field Mapping:**

| MCP Parameter | API Field Name | Type | Required | Notes |
|---------------|----------------|------|----------|-------|
| `project_id` | Path parameter | int | ✅ Yes | Project to update |
| `title` | `title` | string | ❌ No | New title |
| `description` | `description` | string | ❌ No | New description |
| `budget_amount` | `budget_amount` | float | ❌ No | New budget |

**Note:** At least one field must be provided for update.

**Example:**
```python
# MCP Call
dolibarr_update_project(
    project_id=13,
    title="Updated Title",
    budget_amount="75000.00"
)

# API Call
PUT /api/index.php/projects/13
Headers:
  DOLAPIKEY: xxx
  Content-Type: application/json
Body:
{
    "title": "Updated Title",
    "budget_amount": 75000.00
}

# Response: Updated project object
```

---

### 8. Delete Project

| Property | Value |
|----------|-------|
| **MCP Tool** | `dolibarr_delete_project(project_id, confirm)` |
| **HTTP Method** | DELETE |
| **Endpoint** | `/api/index.php/projects/{id}` |
| **Body** | None |
| **Response** | Success indicator (integer) |
| **Timeout** | 10 seconds |
| **Version** | Confirmation added in v1.1.0 |

**Parameters:**

| MCP Parameter | API Mapping | Type | Default | Notes |
|---------------|-------------|------|---------|-------|
| `project_id` | Path parameter | int | (required) | Project to delete |
| `confirm` | Not sent to API | string | "" | ⚠️ Safety feature (v1.1.0+) |

**⚠️ SAFETY FEATURE (v1.1.0):**
- If `confirm != "yes"`, returns warning message and doesn't call API
- Only calls DELETE endpoint when `confirm="yes"`

**Example:**
```python
# MCP Call (without confirmation) - No API call
dolibarr_delete_project(project_id=13)
# Returns: Warning message

# MCP Call (with confirmation) - Calls API
dolibarr_delete_project(project_id=13, confirm="yes")

# API Call
DELETE /api/index.php/projects/13
Headers: DOLAPIKEY: xxx

# Response: 1 (success)
```

---

## Field Mappings

### Project Object Fields

**Response Fields (API → MCP Display):**

| API Field | Display Name | Type | Notes |
|-----------|--------------|------|-------|
| `id` | ID | integer | Numeric project ID |
| `ref` | Reference | string | Project reference code |
| `title` | Project Title | string | Project name |
| `description` | Description | string | Optional |
| `socid` | Third Party ID | string/int | ⚠️ API returns string "1" |
| `fk_soc` | Third Party ID | integer | Alternative field (database) |
| `status` / `statut` / `fk_statut` | Status | integer | 0=Draft, 1=Validated, 2=Closed |
| `budget_amount` | Budget | float | Optional |
| `date_start` | Start Date | timestamp | Unix timestamp → dd/MM/YYYY |
| `date_end` | End Date | timestamp | Unix timestamp → dd/MM/YYYY |

**⚠️ Third Party ID - Special Handling:**

```python
# v1.0.0 (BUG - never displayed)
if project.get('fk_soc'):
    display(project.get('fk_soc'))

# v1.1.0 (FIXED - checks both fields)
third_party_id = project.get('socid') or project.get('fk_soc')
if third_party_id:
    display(third_party_id)
```

**Why both fields?**
- API responses use `socid` (string)
- Direct database access uses `fk_soc` (integer)
- Server now checks both for compatibility

---

### Status Mapping

| Status Code | Dolibarr Status | API Returns | Display |
|-------------|-----------------|-------------|---------|
| 0 | Draft | `"0"` or `0` | Brouillon |
| 1 | Validated | `"1"` or `1` | Validé |
| 2 | Closed | `"2"` or `2` | Fermé |

**Status Field Names:**
- Dolibarr API may return: `status`, `statut`, or `fk_statut`
- Server checks all three fields for maximum compatibility

---

### Date Formatting

**API → MCP Display:**
- API provides: Unix timestamp (integer)
- Display format: `dd/MM/YYYY`
- Example: `1734480000` → `18/12/2025`

**Date Fields:**
- `date_start` - Project start date
- `date_end` - Project end date
- `date_close` - Project close date

---

## HTTP Status Codes

| Status Code | Meaning | MCP Error Message |
|-------------|---------|-------------------|
| 200 | Success | ✅ Operation successful |
| 400 | Bad Request | ❌ Error: Invalid request - {details} |
| 401 | Unauthorized | ❌ Error: Authentication failed or insufficient permissions |
| 404 | Not Found | ❌ Error: Project {id} not found |
| 500 | Server Error | ❌ API Error: 500 - {details} |

---

## SQL Filters

**Used by:** `dolibarr_get_project_by_ref()`

**Syntax:**
```
sqlfilters=(t.ref:=:'VALUE')
```

**Table Prefix:** `t.` refers to the projects table

**Available Operators:**
- `:=:` - Exact match (used for reference search)
- `:like:` - Pattern match
- `:>:` - Greater than
- `:<:` - Less than

**Example Filters:**
```python
# Exact reference
sqlfilters=(t.ref:=:'PJ2512-0001')

# Reference pattern
sqlfilters=(t.ref:like:'PJ2512%')

# By third party
sqlfilters=(t.fk_soc:=:1)

# Multiple filters (AND)
sqlfilters=(t.ref:like:'PJ2512%') AND (t.fk_statut:=:1)
```

---

## URL Generation

**Pattern:**
```
{DOLIBARR_URL}/projet/card.php?id={project_id}
```

**Used in:** All MCP tool responses that include project information

**Example:**
```
http://your-dolibarr/htdocs/projet/card.php?id=13
```

**Task URLs:**
```
{DOLIBARR_URL}/projet/tasks/task.php?id={task_id}
```

---

## Examples

### Complete Create Flow

```python
# 1. MCP Tool Call
result = dolibarr_create_project(
    ref="PJ2512-0015",
    title="Website Redesign",
    description="Complete website overhaul",
    fk_soc="3",                    # Third party ID
    budget_amount="125000.50"
)

# 2. Internal Processing
# - Validate ref and title (required)
# - Convert fk_soc to socid (CRITICAL)
# - Convert budget_amount to float
# - Build request body

# 3. API Request
POST http://your-dolibarr/api/index.php/projects
Headers:
  DOLAPIKEY: your-api-key-here
  Content-Type: application/json
  Accept: application/json
Body:
{
  "ref": "PJ2512-0015",
  "title": "Website Redesign",
  "description": "Complete website overhaul",
  "socid": 3,                      # ← Converted from fk_soc
  "budget_amount": 125000.5
}

# 4. API Response
15

# 5. MCP Response
✅ Project Created Successfully!

   Project ID: 15
   Reference: PJ2512-0015
   Title: Website Redesign
   URL: http://your-dolibarr/htdocs/projet/card.php?id=15
```

---

### Complete Read Flow

```python
# 1. MCP Tool Call
result = dolibarr_get_project(project_id=15)

# 2. API Request
GET http://your-dolibarr/api/index.php/projects/15
Headers:
  DOLAPIKEY: xxx

# 3. API Response
{
  "id": "15",
  "ref": "PJ2512-0015",
  "title": "Website Redesign",
  "description": "Complete website overhaul",
  "socid": "3",                    # ← String format
  "status": "0",
  "budget_amount": "125000.50000000",
  "date_start": "1734480000",
  "date_end": "",
  ...
}

# 4. Processing
# - Map status 0 → "Brouillon"
# - Format date 1734480000 → "18/12/2025"
# - Check socid field for Third Party ID
# - Generate URL

# 5. MCP Response
✅ Project Retrieved:

📊 Project: Website Redesign
   ID: 15
   Reference: PJ2512-0015
   Status: Brouillon
   Description: Complete website overhaul
   Third Party ID: 3               # ← Now displays correctly (v1.1.0)
   Budget: 125000.50000000
   Start Date: 18/12/2025
   URL: http://your-dolibarr/htdocs/projet/card.php?id=15
```

---

## Version Differences

### v1.0.0 → v1.1.0 Changes

| Feature | v1.0.0 | v1.1.0 | Impact |
|---------|--------|--------|--------|
| **Create project with third party** | Sent `fk_soc` (ignored) | Sends `socid` ✅ | Bug fixed |
| **Display Third Party ID** | Never displayed | Displays correctly ✅ | Bug fixed |
| **Delete confirmation** | No confirmation | Requires `confirm="yes"` | Safety added |
| **Search by reference** | Not available | `dolibarr_get_project_by_ref()` | New feature |
| **Auto-pagination** | Manual only | `dolibarr_list_all_projects()` | New feature |

---

## Best Practices

1. **Always provide required fields** when creating projects (ref, title)
2. **Use reference search** when users know the reference code
3. **Use auto-pagination** for complete lists, manual pagination for UI display
4. **Always confirm deletions** by providing `confirm="yes"`
5. **Check both socid and fk_soc** when accessing third party information
6. **Handle all status field variations** (status, statut, fk_statut)
7. **Format dates** for user display (dd/MM/YYYY)
8. **Provide URLs** for easy navigation to Dolibarr interface

---

## Related Documentation

- **CHANGELOG.md** - Version history and release notes
- **ERROR_CODES.md** - Error codes and troubleshooting
- **CLAUDE.md** - Development guidelines and MCP constraints
- **Dolibarr API Docs** - https://wiki.dolibarr.org/index.php/Module_Web_Services_API_REST

---

*Last Updated: 2025-12-18*
*Version: 1.1.0*
