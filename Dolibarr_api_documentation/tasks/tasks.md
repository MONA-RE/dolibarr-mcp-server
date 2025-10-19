# Tasks API

The Tasks API allows you to manage tasks within projects in your Dolibarr instance. You can create, read, update, delete tasks, manage time spent, and retrieve user roles.

## Endpoints

- [Get a task](#get-a-task)
- [List tasks](#list-tasks)
- [Create a task](#create-a-task)
- [Update a task](#update-a-task)
- [Delete a task](#delete-a-task)
- [Get task roles](#get-task-roles)
- [Add time spent](#add-time-spent)

---

## Get a task

Retrieve detailed information about a specific task, optionally including time spent data.

```
GET /tasks/{id}
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the task |
| `includetimespent` | integer | query | No | 0 | 0=Return only task, 1=Include time spent summary, 2=Include detailed time spent lines |

### Permissions Required

- `projet->lire` (read project permission)

### Response

Returns a task object with the following fields:

```json
{
  "id": 10,
  "ref": "TASK001",
  "label": "Design mockups",
  "description": "Create initial design mockups for the website",
  "fk_project": 1,
  "fk_task_parent": 0,
  "date_c": 1704067200,
  "date_start": 1704067200,
  "date_end": 1704326400,
  "planned_workload": 28800,
  "duration_effective": 14400,
  "progress": 50,
  "priority": 5,
  "budget_amount": 5000,
  "note_public": "Public notes",
  "note_private": "Private notes"
}
```

### Time Spent Options

**includetimespent=1** - Adds time spent summary to the task object:
```json
{
  "id": 10,
  "ref": "TASK001",
  "label": "Design mockups",
  "timespent_total_duration": 14400,
  "timespent_nblines": 3,
  "timespent_min_date": "2024-01-01",
  "timespent_max_date": "2024-01-03"
}
```

**includetimespent=2** - Adds detailed time spent lines:
```json
{
  "id": 10,
  "ref": "TASK001",
  "label": "Design mockups",
  "timespent_lines": [
    {
      "id": 1,
      "fk_user": 5,
      "task_date": 1704067200,
      "task_duration": 7200,
      "note": "Initial mockup creation"
    },
    {
      "id": 2,
      "fk_user": 5,
      "task_date": 1704153600,
      "task_duration": 7200,
      "note": "Mockup revisions"
    }
  ]
}
```

### Example Requests

**Get task only:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks/10' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Get task with time spent summary:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks/10?includetimespent=1' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Get task with detailed time spent:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks/10?includetimespent=2' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or access not allowed |
| 404 | Task not found |

---

## List tasks

Retrieve a list of tasks with optional filtering, sorting, and pagination.

```
GET /tasks
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `sortfield` | string | query | No | `t.rowid` | Field to sort by (e.g., 't.ref', 't.label', 't.progress') |
| `sortorder` | string | query | No | `ASC` | Sort order (`ASC` or `DESC`) |
| `limit` | integer | query | No | 100 | Maximum number of tasks to return |
| `page` | integer | query | No | 0 | Page number (0-indexed) |
| `sqlfilters` | string | query | No | - | Additional SQL filters (see syntax below) |

### SQL Filters Syntax

Use the `sqlfilters` parameter to apply custom filters. The filter uses table alias `t` for tasks.

**Examples:**
```
(t.ref:like:'TASK%') and (t.progress:>:'50')
(t.label:like:'%design%') and (t.date_start:>:'1704067200')
(t.fk_project:=:'1') and (t.progress:<:'100')
```

**Operators:** `like`, `=`, `<`, `>`, `<=`, `>=`, `!=`

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
    "fk_project": 1,
    "progress": 50,
    "date_start": 1704067200,
    "date_end": 1704326400
  },
  {
    "id": 11,
    "ref": "TASK002",
    "label": "Frontend development",
    "fk_project": 1,
    "progress": 25,
    "date_start": 1704326400,
    "date_end": 1704931200
  }
]
```

### Example Requests

**Basic list:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**With pagination:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks?limit=50&page=0' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Sort by progress descending:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks?sortfield=t.progress&sortorder=DESC' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter by project:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks?sqlfilters=(t.fk_project:=:1)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Filter incomplete tasks:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks?sqlfilters=(t.progress:<:100)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | No tasks found |
| 503 | Error when retrieving task list or invalid SQL filters |

---

## Create a task

Create a new task within a project.

```
POST /tasks
```

### Permissions Required

- `projet->creer` (create/modify project permission)

### Request Body

Required fields are marked with *

```json
{
  "ref": "TASK003",              // * Task reference (unique)
  "label": "Backend API",        // * Task label/title
  "fk_project": 1,               // * Project ID
  "description": "Develop REST API endpoints",
  "fk_task_parent": 0,           // Parent task ID (0 = root task)
  "date_start": 1704067200,      // Start date (Unix timestamp)
  "date_end": 1706745600,        // End date (Unix timestamp)
  "planned_workload": 144000,    // Planned workload in seconds (40 hours)
  "progress": 0,                 // Progress percentage (0-100)
  "priority": 5,                 // Priority level
  "budget_amount": 15000,        // Budget for this task
  "note_public": "Public notes",
  "note_private": "Private notes"
}
```

### Response

Returns the ID of the created task:

```json
12
```

### Example Request

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/tasks' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "ref": "TASK003",
    "label": "Backend API Development",
    "fk_project": 1,
    "description": "Develop REST API endpoints for user management",
    "date_start": 1704067200,
    "date_end": 1706745600,
    "planned_workload": 144000,
    "progress": 0,
    "priority": 5
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Missing required field (ref, label, or fk_project) |
| 401 | Insufficient rights |
| 500 | Error creating task |

---

## Update a task

Update an existing task's general fields. This endpoint does NOT update time spent data.

```
PUT /tasks/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the task to update |

### Permissions Required

- `projet->creer` (create/modify project permission)

### Request Body

Send only the fields you want to update:

```json
{
  "label": "Updated Task Label",
  "description": "Updated description",
  "progress": 75,
  "priority": 8,
  "budget_amount": 20000,
  "date_end": 1707350400
}
```

### Response

Returns the updated task object:

```json
{
  "id": 10,
  "ref": "TASK001",
  "label": "Updated Task Label",
  "description": "Updated description",
  "progress": 75,
  "priority": 8,
  "budget_amount": 20000,
  "date_end": 1707350400
}
```

### Example Request

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/tasks/10' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "label": "Design mockups - Phase 2",
    "progress": 75,
    "priority": 8
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Task not found |
| 500 | Error updating task |

---

## Delete a task

Delete a task from the system.

```
DELETE /tasks/{id}
```

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | integer | path | Yes | ID of the task to delete |

### Permissions Required

- `projet->supprimer` (delete project permission)

### Response

```json
{
  "success": {
    "code": 200,
    "message": "Task deleted"
  }
}
```

### Example Request

```bash
curl -X DELETE \
  'https://your-dolibarr.com/api/index.php/tasks/10' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission |
| 404 | Task not found |
| 500 | Error when deleting task |

---

## Get task roles

Retrieve the roles assigned to a user for a specific task.

```
GET /tasks/{id}/roles
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the task |
| `userid` | integer | query | No | 0 | ID of the user (0 = connected user) |

### Permissions Required

- `projet->lire` (read project permission)

### Response

Returns an array of role objects assigned to the user for this task:

```json
[
  {
    "id": 1,
    "code": "TASKEXECUTE",
    "label": "Task Executor"
  },
  {
    "id": 2,
    "code": "TASKCONTRIBUTOR",
    "label": "Task Contributor"
  }
]
```

### Example Requests

**Get roles for connected user:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks/10/roles' \
  -H 'DOLAPIKEY: your_api_key_here'
```

**Get roles for specific user:**
```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks/10/roles?userid=5' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | User doesn't have permission or access not allowed |
| 404 | Task not found |

---

## Add time spent

Add a time spent entry to a task. Time is recorded with date, duration, user, and optional notes.

```
POST /tasks/{id}/addtimespent
```

### Parameters

| Parameter | Type | Location | Required | Default | Description |
|-----------|------|----------|----------|---------|-------------|
| `id` | integer | path | Yes | - | ID of the task |
| `date` | datetime | body | Yes | - | Date and time in format 'YYYY-MM-DD HH:MI:SS' (GMT) |
| `duration` | integer | body | Yes | - | Duration in seconds (3600 = 1 hour) |
| `user_id` | integer | body | No | 0 | User ID (0 = connected user) |
| `note` | string | body | No | '' | Note/comment for this time entry |

### Permissions Required

- `projet->creer` (create/modify project permission)

### Request Body

```json
{
  "date": "2024-01-15 14:30:00",
  "duration": 7200,
  "user_id": 5,
  "note": "Worked on API endpoint implementation"
}
```

### Duration Examples

| Duration | Seconds |
|----------|---------|
| 15 minutes | 900 |
| 30 minutes | 1800 |
| 1 hour | 3600 |
| 2 hours | 7200 |
| 4 hours | 14400 |
| 8 hours | 28800 |

### Response

```json
{
  "success": {
    "code": 200,
    "message": "Time spent added"
  }
}
```

### Example Requests

**Add 4 hours of work:**
```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/tasks/10/addtimespent' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "date": "2024-01-15 09:00:00",
    "duration": 14400,
    "user_id": 0,
    "note": "Frontend development - component creation"
  }'
```

**Add time for specific user:**
```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/tasks/10/addtimespent' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "date": "2024-01-15 14:00:00",
    "duration": 3600,
    "user_id": 5,
    "note": "Code review"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| 304 | Error nothing done - may be task is already validated or locked |
| 401 | User doesn't have permission or access not allowed to project |
| 404 | Task not found |
| 500 | Error when adding time |

---

## Task Object

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | Read-only | Task ID |
| `ref` | string | Yes | Task reference (unique) |
| `label` | string | Yes | Task label/title |
| `description` | string | No | Task description |
| `fk_project` | integer | Yes | Project ID |
| `fk_task_parent` | integer | No | Parent task ID (0 = root task) |
| `date_c` | integer | Read-only | Creation date (Unix timestamp) |
| `date_start` | integer | No | Start date (Unix timestamp) |
| `date_end` | integer | No | End date (Unix timestamp) |
| `planned_workload` | integer | No | Planned workload in seconds |
| `duration_effective` | integer | Read-only | Actual duration spent in seconds |
| `progress` | integer | No | Progress percentage (0-100) |
| `priority` | integer | No | Priority level |
| `budget_amount` | float | No | Budget amount for task |
| `note_public` | string | No | Public notes |
| `note_private` | string | No | Private notes |
| `fk_user_creat` | integer | Read-only | User who created the task |
| `fk_user_valid` | integer | Read-only | User who validated the task |
| `array_options` | object | No | Custom fields (extra fields) |

### Status Values (fk_statut)

| Value | Description |
|-------|-------------|
| 0 | Draft |
| 1 | Validated/Active |

### Time Fields

When using `includetimespent` parameter:

| Field | Type | Description |
|-------|------|-------------|
| `timespent_total_duration` | integer | Total time spent in seconds |
| `timespent_nblines` | integer | Number of time entries |
| `timespent_min_date` | string | Earliest time entry date |
| `timespent_max_date` | string | Latest time entry date |
| `timespent_total_amount` | float | Total cost of time spent |
| `timespent_thm` | float | Average hourly rate |
| `timespent_lines` | array | Array of time spent entries (when includetimespent=2) |

---

## Workload Calculations

### Converting Hours to Seconds

Dolibarr stores workload and duration in seconds.

| Hours | Calculation | Seconds |
|-------|-------------|---------|
| 1 hour | 1 × 3600 | 3600 |
| 4 hours | 4 × 3600 | 14400 |
| 8 hours (1 day) | 8 × 3600 | 28800 |
| 40 hours (1 week) | 40 × 3600 | 144000 |
| 160 hours (1 month) | 160 × 3600 | 576000 |

### JavaScript Helper

```javascript
function hoursToSeconds(hours) {
  return hours * 3600;
}

function secondsToHours(seconds) {
  return seconds / 3600;
}

// Example usage
const plannedWorkload = hoursToSeconds(40); // 144000 seconds (1 week)
const duration = hoursToSeconds(4); // 14400 seconds (4 hours)
```

### PHP Helper

```php
function hoursToSeconds($hours) {
    return $hours * 3600;
}

function secondsToHours($seconds) {
    return $seconds / 3600;
}

// Example usage
$plannedWorkload = hoursToSeconds(40); // 144000 seconds (1 week)
$duration = hoursToSeconds(4); // 14400 seconds (4 hours)
```

---

## Task Hierarchy

Tasks can be organized hierarchically using the `fk_task_parent` field.

### Creating a Task Hierarchy

```json
// Root task
{
  "ref": "TASK001",
  "label": "Phase 1: Design",
  "fk_project": 1,
  "fk_task_parent": 0
}

// Sub-task
{
  "ref": "TASK001-1",
  "label": "Create wireframes",
  "fk_project": 1,
  "fk_task_parent": 10  // ID of TASK001
}

// Another sub-task
{
  "ref": "TASK001-2",
  "label": "Design mockups",
  "fk_project": 1,
  "fk_task_parent": 10  // ID of TASK001
}
```

---

## Notes

- External users can only access tasks for projects linked to their third party (company)
- Internal users can only see tasks of projects they have access to
- The `id` field cannot be modified when updating a task
- Time spent entries cannot be updated through the PUT endpoint - use the dedicated time tracking features
- Some fields are automatically cleaned from the response for security reasons
- All dates use Unix timestamps (seconds since January 1, 1970)
- Duration and workload values are stored in seconds
- Progress is a percentage value between 0 and 100
- When deleting a task, all associated time spent entries are also deleted

---

## Related Documentation

- [Projects API](./projects.md) - Manage projects that contain tasks
- [Task API Fields](./tasks/api_fields_task.md) - Complete list of task fields returned by the API

---

## Common Use Cases

### Get all tasks for a project

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks?sqlfilters=(t.fk_project:=:1)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Get incomplete tasks

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks?sqlfilters=(t.progress:<:100)' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Get tasks with time tracking

```bash
curl -X GET \
  'https://your-dolibarr.com/api/index.php/tasks/10?includetimespent=2' \
  -H 'DOLAPIKEY: your_api_key_here'
```

### Update task progress

```bash
curl -X PUT \
  'https://your-dolibarr.com/api/index.php/tasks/10' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{"progress": 75}'
```

### Track time on a task

```bash
curl -X POST \
  'https://your-dolibarr.com/api/index.php/tasks/10/addtimespent' \
  -H 'DOLAPIKEY: your_api_key_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "date": "2024-01-15 09:00:00",
    "duration": 28800,
    "note": "Full day of development work"
  }'
```
