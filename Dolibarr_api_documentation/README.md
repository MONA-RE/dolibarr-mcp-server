# Dolibarr API Documentation

Welcome to the Dolibarr API documentation. This REST API allows you to interact with your Dolibarr installation programmatically.

## Overview

The Dolibarr API is a RESTful API that accepts and returns JSON-encoded data. It uses standard HTTP methods (GET, POST, PUT, DELETE) and HTTP response codes to indicate API success or errors.

## Base URL

```
https://your-dolibarr-instance.com/api/index.php
```

## Authentication

The Dolibarr API uses API token authentication. You need to include your API key in the request header:

```
DOLAPIKEY: your_api_key_here
```

### Getting your API Key

1. Log in to your Dolibarr instance
2. Go to Home → Setup → Modules
3. Enable the API/Web Services module
4. Go to your user profile
5. Generate an API key in the API section

## Request Format

- **Content-Type**: `application/json`
- **Accept**: `application/json`

All requests should include the `Content-Type: application/json` header when sending data.

## Response Format

The API returns JSON-encoded responses. Fields with `null` values may be omitted from the response.

### Success Response

Successful requests return a 2xx status code with the requested data:

```json
{
  "id": 1,
  "ref": "PROJ001",
  "title": "My Project",
  ...
}
```

### Error Response

Error responses include a status code (4xx or 5xx) and error details:

```json
{
  "error": {
    "code": 401,
    "message": "Access not allowed for login username"
  }
}
```

## HTTP Status Codes

- **200 OK** - Request successful
- **201 Created** - Resource created successfully
- **304 Not Modified** - Resource not modified
- **400 Bad Request** - Invalid request (missing required fields)
- **401 Unauthorized** - Authentication failed or insufficient permissions
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error
- **503 Service Unavailable** - Service temporarily unavailable

## Available Endpoints

### Projects

Manage projects in your Dolibarr instance.

- [Projects API Documentation](./projects.md)

## Permissions

API access is controlled by user permissions in Dolibarr. The user whose API key is used must have appropriate permissions to perform operations:

- **Read**: `projet->lire` permission
- **Create**: `projet->creer` permission
- **Delete**: `projet->supprimer` permission

## Pagination

List endpoints support pagination using the following parameters:

- `limit` - Number of records to return (default: 100)
- `page` - Page number (0-indexed)

Example:
```
GET /projects?limit=50&page=0
```

## Filtering

Some endpoints support filtering using the `sqlfilters` parameter. The syntax uses the format:

```
(t.field_name:operator:'value')
```

Multiple filters can be combined with `and` or `or`:

```
(t.ref:like:'PROJ%') and (t.date_creation:<:'20231231')
```

## Date Format

Dates should be provided in Unix timestamp format or ISO 8601 format.

## Support

For more information about Dolibarr, visit [dolibarr.org](https://www.dolibarr.org/)
