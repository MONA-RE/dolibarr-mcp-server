# Projects API

The Projects API allows you to manage projects in your Dolibarr instance. You can create, read, update, delete projects, and manage their tasks.

## Endpoints

- [Get a project](#get-a-project)
- [List projects](#list-projects)
- [Create a project](#create-a-project)
- [Update a project](#update-a-project)
- [Delete a project](#delete-a-project)
- [Validate a project](#validate-a-project)
- [Get project tasks](#get-project-tasks)
- [Get project roles](#get-project-roles)

---

## Get a project

Retrieve detailed information about a specific project.

```
GET /projects/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the project |

### Permissions Required

- `projet->lire` (read project permission)

### Response

Returns a project object with the following fields:

```json
{
  "id": 1,
  "ref": "PROJ001",
  "title": "Website Redesign",
  "description": "Complete redesign of company website",
  "fk_soc": 5,
  "public": 0,
  "date_start": 1704067200,
  "date_end": 1706745600,
  "fk_statut": 1,
  "budget_amount": 50000,
  "usage_bill_time": 1,
  "usage_organize_event": 0
}
```

### Example Request

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or access not allowed |
| 404 | Project not found |

---

## List projects

Retrieve a list of projects with optional filtering and pagination.

```
GET /projects
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `sortfield` | string | query | No | `t.rowid` | Field to sort by |
| `sortorder` | string | query | No | `ASC` | Sort order (`ASC` or `DESC`) |
| `limit` | integer | query | No | 100 | Maximum number of projects to return |
| `page` | integer | query | No | 0 | Page number (0-indexed) |
| `thirdparty_ids` | string | query | No | - | Filter by third party IDs (comma-separated, e.g., '1,2,3') |
| `category` | integer | query | No | 0 | Filter by category ID |
| `sqlfilters` | string | query | No | - | Additional SQL filters |

### SQL Filters Syntax

Use the `sqlfilters` parameter to apply custom filters:

```
(t.ref:like:'PROJ%') and (t.date_creation:<:'20231231')
```

Operators: `like`, `=`, `<`, `>`, `<=`, `>=`, `!=`

### Permissions Required

- `projet->lire` (read project permission)

### Response

Returns an array of project objects:

```json
[
  {
    "id": 1,
    "ref": "PROJ001",
    "title": "Website Redesign",
    "fk_soc": 5,
    "fk_statut": 1
  },
  {
    "id": 2,
    "ref": "PROJ002",
    "title": "Mobile App Development",
    "fk_soc": 8,
    "fk_statut": 1
  }
]
```

### Example Requests

**Basic list:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With pagination:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects?limit=50&page=0' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by third party:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects?thirdparty_ids=5,8' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With SQL filters:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects?sqlfilters=(t.ref:like:%27PROJ%25%27)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No projects found |
| 503 | Error when retrieving project list |

---

## Create a project

Create a new project.

```
POST /projects
```

### Permissions Required

- `projet->creer` (create project permission)

### Request Body

Required fields are marked with *

```json
{
  "ref": "PROJ003",          // * Project reference
  "title": "New Project",    // * Project title
  "description": "Project description",
  "fk_soc": 5,              // Third party ID
  "public": 0,              // 0=Private, 1=Public
  "date_start": 1704067200, // Unix timestamp
  "date_end": 1706745600,   // Unix timestamp
  "budget_amount": 25000,
  "usage_bill_time": 1,
  "usage_organize_event": 0
}
```

### Response

Returns the ID of the created project:

```json
3
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/projects' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "ref": "PROJ003",
    "title": "New Marketing Campaign",
    "description": "Q1 2024 Marketing Campaign",
    "fk_soc": 5,
    "public": 0,
    "date_start": 1704067200,
    "budget_amount": 25000
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing required field (ref or title) |
| 401 | Insufficient rights |
| 500 | Error creating project |

---

## Update a project

Update an existing project's general fields.

```
PUT /projects/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the project to update |

### Permissions Required

- `projet->creer` (create/modify project permission)

### Request Body

Send only the fields you want to update:

```json
{
  "title": "Updated Project Title",
  "description": "Updated description",
  "budget_amount": 60000,
  "fk_statut": 1
}
```

### Response

Returns the updated project object:

```json
{
  "id": 1,
  "ref": "PROJ001",
  "title": "Updated Project Title",
  "description": "Updated description",
  "budget_amount": 60000,
  "fk_statut": 1
}
```

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/projects/1' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Website Redesign - Phase 2",
    "budget_amount": 75000
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Project not found |
| 500 | Error updating project |

---

## Delete a project

Delete a project from the system.

```
DELETE /projects/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the project to delete |

### Permissions Required

- `projet->supprimer` (delete project permission)

### Response

```json
{
  "success": {
    "code": 200,
    "message": "Project deleted"
  }
}
```

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/projects/1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Project not found |
| 500 | Error when deleting project |

---

## Validate a project

Validate a project (change its status to validated).

```
POST /projects/{id}/validate
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the project |
| `notrigger` | integer | body | No | 0 | 1=Don't execute triggers, 0=Execute triggers |

### Permissions Required

- `projet->creer` (create/modify project permission)

### Request Body

```json
{
  "notrigger": 0
}
```

**Note:** Due to a known issue, sending an empty body may result in a 403 error. Always include the `notrigger` parameter.

### Response

```json
{
  "success": {
    "code": 200,
    "message": "Project validated"
  }
}
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/projects/1/validate' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "notrigger": 0
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 304 | Nothing done - object may already be validated |
| 401 | User doesn't have permission |
| 403 | Content type not supported (send JSON body) |
| 404 | Project not found |
| 500 | Error when validating project |

---

## Get project tasks

Retrieve all tasks associated with a project. See also the separate [Tasks API](./tasks.md) for more task operations.

```
GET /projects/{id}/tasks
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the project |
| `includetimespent` | integer | query | No | 0 | 0=Tasks only, 1=Include time spent summary, 2=Include detailed time spent lines |

### Permissions Required

- `projet->lire` (read project permission)

### Response

Returns an array of task objects:

```json
[
  {
    "id": 10,
    "ref": "TASK001",
    "label": "Design mockups",
    "description": "Create initial design mockups",
    "fk_project": 1,
    "dateo": 1704067200,
    "datee": 1704326400,
    "planned_workload": 28800,
    "progress": 50
  },
  {
    "id": 11,
    "ref": "TASK002",
    "label": "Frontend development",
    "fk_project": 1,
    "progress": 25
  }
]
```

### Example Requests

**Get tasks only:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects/1/tasks' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Get tasks with time spent summary:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects/1/tasks?includetimespent=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Get tasks with detailed time spent:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects/1/tasks?includetimespent=2' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Project not found |

---

## Get project roles

Retrieve the roles assigned to a user for a specific project.

```
GET /projects/{id}/roles
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the project |
| `userid` | integer | query | No | 0 | ID of the user (0 = connected user) |

### Permissions Required

- `projet->lire` (read project permission)

### Response

Returns an array of role objects:

```json
[
  {
    "id": 1,
    "code": "PROJECTLEADER",
    "label": "Project Leader"
  },
  {
    "id": 2,
    "code": "CONTRIBUTOR",
    "label": "Contributor"
  }
]
```

### Example Requests

**Get roles for connected user:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects/1/roles' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Get roles for specific user:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/projects/1/roles?userid=5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Project not found |

---

## Project Object

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Project ID |
| `ref` | string | Project reference (unique) |
| `title` | string | Project title |
| `description` | string | Project description |
| `fk_soc` | integer | Third party (company) ID |
| `public` | integer | 0=Private, 1=Public |
| `date_start` | integer | Start date (Unix timestamp) |
| `date_end` | integer | End date (Unix timestamp) |
| `fk_statut` | integer | Project status |
| `budget_amount` | float | Budget amount |
| `usage_bill_time` | integer | Use project to bill time spent |
| `usage_organize_event` | integer | Use project to organize events |
| `array_options` | object | Custom fields (extra fields) |

### Status Values

| Value | Description |
|-------|-------------|
| 0 | Draft |
| 1 | Validated/Open |
| 2 | Closed |

---

## Notes

- External users can only access projects linked to their third party (company)
- Internal users can only see projects of customers they manage, unless they have the "See all" permission
- The `id` field cannot be modified when updating a project
- Some fields are automatically cleaned from the response for security reasons
