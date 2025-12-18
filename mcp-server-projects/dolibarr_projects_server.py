#!/usr/bin/env python3
"""
Simple Dolibarr Projects MCP Server - Manage Dolibarr projects via MCP
"""
import os
import sys
import logging
import json
from datetime import datetime, timezone
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("dolibarr-projects-server")

# Initialize MCP server
mcp = FastMCP("dolibarr_projects")

# Configuration
DOLIBARR_URL = os.environ.get("DOLIBARR_URL", "")
DOLIBARR_API_KEY = os.environ.get("DOLIBARR_API_KEY", "")

# === UTILITY FUNCTIONS ===

def get_headers():
    """Get HTTP headers for Dolibarr API requests."""
    return {
        "DOLAPIKEY": DOLIBARR_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def get_project_status(fk_statut):
    """Convert project status code to human-readable label."""
    status_map = {
        0: "Brouillon",
        1: "Validé",
        2: "Fermé",
        "0": "Brouillon",
        "1": "Validé",
        "2": "Fermé",
    }
    return status_map.get(fk_statut, f"Inconnu ({fk_statut})")

def format_date(timestamp):
    """Convert Unix timestamp to dd/MM/YYYY format."""
    if not timestamp:
        return None
    try:
        # Convert to int if it's a string
        ts = int(timestamp) if isinstance(timestamp, str) else timestamp
        # Convert Unix timestamp to datetime
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        # Format as dd/MM/YYYY
        return dt.strftime("%d/%m/%Y")
    except (ValueError, TypeError, OSError):
        # Return original value if conversion fails
        return str(timestamp)

def format_project_info(project):
    """Format project data for display."""
    # Get status with proper mapping (API returns 'status' or 'statut', not 'fk_statut')
    status_value = project.get('status') or project.get('statut') or project.get('fk_statut')
    status_label = get_project_status(status_value) if status_value is not None else 'N/A'

    lines = [
        f"📊 Project: {project.get('title', 'N/A')}",
        f"   ID: {project.get('id', 'N/A')}",
        f"   Reference: {project.get('ref', 'N/A')}",
        f"   Status: {status_label}",
    ]

    if project.get('description'):
        lines.append(f"   Description: {project.get('description')}")

    third_party_id = project.get('socid') or project.get('fk_soc')
    if third_party_id:
        lines.append(f"   Third Party ID: {third_party_id}")

    if project.get('budget_amount'):
        lines.append(f"   Budget: {project.get('budget_amount')}")

    if project.get('date_start'):
        formatted_date = format_date(project.get('date_start'))
        if formatted_date:
            lines.append(f"   Start Date: {formatted_date}")

    if project.get('date_end'):
        formatted_date = format_date(project.get('date_end'))
        if formatted_date:
            lines.append(f"   End Date: {formatted_date}")

    # Add URL to project
    project_id = project.get('id', 'N/A')
    if DOLIBARR_URL and project_id != 'N/A':
        lines.append(f"   URL: {DOLIBARR_URL}/projet/card.php?id={project_id}")

    return "\n".join(lines)

# === MCP TOOLS ===

@mcp.tool()
async def dolibarr_get_project(project_id: int) -> str:
    """Get details of a specific Dolibarr project by ID."""
    logger.info(f"Fetching project with ID: {project_id}")

    if not project_id or project_id <= 0:
        return "❌ Error: project_id is required and must be a positive integer"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/projects/{project_id}"
            response = await client.get(url, headers=get_headers(), timeout=10)
            response.raise_for_status()
            project = response.json()

            return f"✅ Project Retrieved:\n\n{format_project_info(project)}"

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Error: Project {project_id} not found"
        elif e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error fetching project: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_get_project_by_ref(ref: str = "") -> str:
    """Get a Dolibarr project by its reference code."""
    logger.info(f"Fetching project with reference: {ref}")

    if not ref.strip():
        return "❌ Error: ref (project reference) is required"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        # Build SQL filter to search by reference
        sql_filter = f"(t.ref:=:'{ref.strip()}')"

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/projects"
            params = {"sqlfilters": sql_filter}
            response = await client.get(url, headers=get_headers(), params=params, timeout=10)
            response.raise_for_status()
            projects = response.json()

            # Check if a project was found
            if not projects or len(projects) == 0:
                return f"❌ Error: Project with reference '{ref}' not found"

            # Get first project (reference is unique)
            project = projects[0]

            return f"✅ Project Retrieved:\n\n{format_project_info(project)}"

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Error: Project with reference '{ref}' not found"
        elif e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error fetching project by reference: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_list_projects(limit: str = "100", page: str = "0", sortfield: str = "t.rowid", sortorder: str = "ASC") -> str:
    """List Dolibarr projects with optional pagination and sorting."""
    logger.info(f"Listing projects: limit={limit}, page={page}")

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        limit_int = int(limit) if limit.strip() else 100
        page_int = int(page) if page.strip() else 0

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/projects"
            params = {
                "limit": limit_int,
                "page": page_int,
                "sortfield": sortfield if sortfield.strip() else "t.rowid",
                "sortorder": sortorder if sortorder.strip() else "ASC"
            }

            response = await client.get(url, headers=get_headers(), params=params, timeout=10)
            response.raise_for_status()
            projects = response.json()

            if not projects:
                return "📊 No projects found"

            result_lines = [f"✅ Found {len(projects)} project(s):\n"]
            for project in projects:
                project_id = project.get('id', 'N/A')
                project_url = f"{DOLIBARR_URL}/projet/card.php?id={project_id}" if DOLIBARR_URL and project_id != 'N/A' else "N/A"

                # Get status with proper mapping (API returns 'status' or 'statut', not 'fk_statut')
                status_value = project.get('status') or project.get('statut') or project.get('fk_statut')
                status_label = get_project_status(status_value) if status_value is not None else 'N/A'

                result_lines.append(f"• {project.get('ref', 'N/A')} - {project.get('title', 'N/A')} (ID: {project_id}) - Status: {status_label} - URL: {project_url}")

            return "\n".join(result_lines)

    except ValueError as e:
        return f"❌ Error: Invalid number format - {str(e)}"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        elif e.response.status_code == 404:
            return "📊 No projects found"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_list_all_projects(sortfield: str = "t.rowid", sortorder: str = "ASC") -> str:
    """List ALL Dolibarr projects with automatic pagination."""
    logger.info(f"Listing all projects with automatic pagination")

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    all_projects = []
    page = 0
    limit = 100

    try:
        async with httpx.AsyncClient() as client:
            while True:
                # Fetch one page
                url = f"{DOLIBARR_URL}/api/index.php/projects"
                params = {
                    "sortfield": sortfield if sortfield.strip() else "t.rowid",
                    "sortorder": sortorder if sortorder.strip() else "ASC",
                    "limit": limit,
                    "page": page
                }

                response = await client.get(url, headers=get_headers(), params=params, timeout=30)
                response.raise_for_status()
                projects = response.json()

                # If no projects, stop
                if not projects or len(projects) == 0:
                    break

                # Add projects to complete list
                all_projects.extend(projects)

                # If less than limit projects, it's the last page
                if len(projects) < limit:
                    break

                # Move to next page
                page += 1

        # Check if we found any projects
        if not all_projects:
            return "📊 No projects found"

        # Format output
        result_lines = [f"✅ Found {len(all_projects)} project(s) (all pages):\n"]
        for project in all_projects:
            project_id = project.get('id', 'N/A')
            project_url = f"{DOLIBARR_URL}/projet/card.php?id={project_id}" if DOLIBARR_URL and project_id != 'N/A' else "N/A"

            # Get status with proper mapping
            status_value = project.get('status') or project.get('statut') or project.get('fk_statut')
            status_label = get_project_status(status_value) if status_value is not None else 'N/A'

            result_lines.append(f"• {project.get('ref', 'N/A')} - {project.get('title', 'N/A')} (ID: {project_id}) - Status: {status_label} - URL: {project_url}")

        return "\n".join(result_lines)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error listing all projects: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_create_project(ref: str = "", title: str = "", description: str = "", fk_soc: str = "", budget_amount: str = "") -> str:
    """Create a new Dolibarr project with required ref and title."""
    logger.info(f"Creating project: {ref} - {title}")

    if not ref.strip():
        return "❌ Error: ref (project reference) is required"

    if not title.strip():
        return "❌ Error: title is required"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        project_data = {
            "ref": ref.strip(),
            "title": title.strip()
        }

        if description.strip():
            project_data["description"] = description.strip()

        if fk_soc.strip():
            try:
                project_data["socid"] = int(fk_soc)
            except ValueError:
                return f"❌ Error: fk_soc must be a valid integer, got: {fk_soc}"

        if budget_amount.strip():
            try:
                project_data["budget_amount"] = float(budget_amount)
            except ValueError:
                return f"❌ Error: budget_amount must be a valid number, got: {budget_amount}"

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/projects"
            response = await client.post(url, headers=get_headers(), json=project_data, timeout=10)
            response.raise_for_status()
            project_id = response.json()

            # Build URL to the created project
            project_url = f"{DOLIBARR_URL}/projet/card.php?id={project_id}" if DOLIBARR_URL else "N/A"

            return f"✅ Project Created Successfully!\n\n   Project ID: {project_id}\n   Reference: {ref}\n   Title: {title}\n   URL: {project_url}"

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        elif e.response.status_code == 400:
            return f"❌ Error: Invalid request - {e.response.text}"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_update_project(project_id: int, title: str = "", description: str = "", budget_amount: str = "") -> str:
    """Update an existing Dolibarr project by ID."""
    logger.info(f"Updating project: {project_id}")

    if not project_id or project_id <= 0:
        return "❌ Error: project_id is required and must be a positive integer"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    update_data = {}

    if title.strip():
        update_data["title"] = title.strip()

    if description.strip():
        update_data["description"] = description.strip()

    if budget_amount.strip():
        try:
            update_data["budget_amount"] = float(budget_amount)
        except ValueError:
            return f"❌ Error: budget_amount must be a valid number, got: {budget_amount}"

    if not update_data:
        return "❌ Error: At least one field to update must be provided (title, description, or budget_amount)"

    try:
        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/projects/{project_id}"
            response = await client.put(url, headers=get_headers(), json=update_data, timeout=10)
            response.raise_for_status()
            updated_project = response.json()

            return f"✅ Project Updated Successfully:\n\n{format_project_info(updated_project)}"

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Error: Project {project_id} not found"
        elif e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_delete_project(project_id: int, confirm: str = "") -> str:
    """Delete a Dolibarr project by ID (requires confirm='yes' for safety)."""
    logger.info(f"Deleting project: {project_id}")

    if not project_id or project_id <= 0:
        return "❌ Error: project_id is required and must be a positive integer"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    # Check confirmation
    if confirm.lower() != "yes":
        return (
            f"⚠️ Warning: This will permanently delete project {project_id}.\n"
            f"This action is irreversible and will remove all project data.\n\n"
            f"To confirm deletion, call this tool again with: confirm='yes'"
        )

    try:
        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/projects/{project_id}"
            response = await client.delete(url, headers=get_headers(), timeout=10)
            response.raise_for_status()
            result = response.json()

            return f"✅ Project {project_id} deleted successfully"

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Error: Project {project_id} not found"
        elif e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_get_project_tasks(project_id: int, includetimespent: int = 0) -> str:
    """Get all tasks for a specific Dolibarr project."""
    logger.info(f"Fetching tasks for project: {project_id}")

    if not project_id or project_id <= 0:
        return "❌ Error: project_id is required and must be a positive integer"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        # includetimespent is already an int from the parameter type
        if includetimespent not in [0, 1, 2]:
            return "❌ Error: includetimespent must be 0, 1, or 2"

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/projects/{project_id}/tasks"
            params = {"includetimespent": includetimespent}

            response = await client.get(url, headers=get_headers(), params=params, timeout=10)
            response.raise_for_status()
            tasks = response.json()

            if not tasks:
                return f"📊 No tasks found for project {project_id}"

            result_lines = [f"✅ Found {len(tasks)} task(s) for project {project_id}:\n"]
            for task in tasks:
                task_id = task.get('id', 'N/A')
                task_url = f"{DOLIBARR_URL}/projet/tasks/task.php?id={task_id}" if DOLIBARR_URL and task_id != 'N/A' else "N/A"
                task_line = f"• {task.get('ref', 'N/A')} - {task.get('label', 'N/A')} (ID: {task_id})"
                if task.get('progress'):
                    task_line += f" - Progress: {task.get('progress')}%"
                task_line += f" - URL: {task_url}"
                result_lines.append(task_line)

            return "\n".join(result_lines)

    except ValueError as e:
        return f"❌ Error: Invalid number format - {str(e)}"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Error: Project {project_id} not found"
        elif e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error fetching tasks: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting Dolibarr Projects MCP server...")

    if not DOLIBARR_URL:
        logger.warning("DOLIBARR_URL not set - server will return errors until configured")
    if not DOLIBARR_API_KEY:
        logger.warning("DOLIBARR_API_KEY not set - server will return errors until configured")

    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
