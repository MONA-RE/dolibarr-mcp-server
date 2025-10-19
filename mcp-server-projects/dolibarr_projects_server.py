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

def format_project_info(project):
    """Format project data for display."""
    lines = [
        f"📊 Project: {project.get('title', 'N/A')}",
        f"   ID: {project.get('id', 'N/A')}",
        f"   Reference: {project.get('ref', 'N/A')}",
        f"   Status: {project.get('fk_statut', 'N/A')}",
    ]

    if project.get('description'):
        lines.append(f"   Description: {project.get('description')}")

    if project.get('fk_soc'):
        lines.append(f"   Third Party ID: {project.get('fk_soc')}")

    if project.get('budget_amount'):
        lines.append(f"   Budget: {project.get('budget_amount')}")

    if project.get('date_start'):
        lines.append(f"   Start Date: {project.get('date_start')}")

    if project.get('date_end'):
        lines.append(f"   End Date: {project.get('date_end')}")

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
                result_lines.append(f"• {project.get('ref', 'N/A')} - {project.get('title', 'N/A')} (ID: {project.get('id', 'N/A')})")

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
                project_data["fk_soc"] = int(fk_soc)
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

            return f"✅ Project Created Successfully!\n\n   Project ID: {project_id}\n   Reference: {ref}\n   Title: {title}"

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
async def dolibarr_delete_project(project_id: int) -> str:
    """Delete a Dolibarr project by ID."""
    logger.info(f"Deleting project: {project_id}")

    if not project_id or project_id <= 0:
        return "❌ Error: project_id is required and must be a positive integer"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

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
        timespent_int = int(includetimespent) if includetimespent.strip() else 0

        if timespent_int not in [0, 1, 2]:
            return "❌ Error: includetimespent must be 0, 1, or 2"

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/projects/{project_id}/tasks"
            params = {"includetimespent": timespent_int}

            response = await client.get(url, headers=get_headers(), params=params, timeout=10)
            response.raise_for_status()
            tasks = response.json()

            if not tasks:
                return f"📊 No tasks found for project {project_id}"

            result_lines = [f"✅ Found {len(tasks)} task(s) for project {project_id}:\n"]
            for task in tasks:
                task_line = f"• {task.get('ref', 'N/A')} - {task.get('label', 'N/A')} (ID: {task.get('id', 'N/A')})"
                if task.get('progress'):
                    task_line += f" - Progress: {task.get('progress')}%"
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
