#!/usr/bin/env python3
"""
Simple Dolibarr Tasks MCP Server - Manage Dolibarr project tasks via MCP
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
logger = logging.getLogger("dolibarr-tasks-server")

# Initialize MCP server
mcp = FastMCP("dolibarr_tasks")

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

def format_task_info(task):
    """Format task data for display."""
    lines = [
        f"📋 Task: {task.get('label', 'N/A')}",
        f"   ID: {task.get('id', 'N/A')}",
        f"   Ref: {task.get('ref', 'N/A')}",
        f"   Project ID: {task.get('fk_project', 'N/A')}",
    ]

    if task.get('fk_task_parent'):
        lines.append(f"   Parent task ID: {task.get('fk_task_parent')}")

    if task.get('description'):
        lines.append(f"   Description: {task.get('description')}")

    if task.get('progress') is not None:
        lines.append(f"   Progress: {task.get('progress')}%")

    if task.get('priority') is not None:
        lines.append(f"   Priority: {task.get('priority')}")

    if task.get('planned_workload'):
        hours = int(task.get('planned_workload')) / 3600
        lines.append(f"   Planned workload: {hours:.2f} hours")

    if task.get('duration_effective'):
        hours = int(task.get('duration_effective')) / 3600
        lines.append(f"   Effective duration: {hours:.2f} hours")

    if task.get('budget_amount'):
        lines.append(f"   Budget: {task.get('budget_amount')}")

    if task.get('date_start'):
        lines.append(f"   Start date: {task.get('date_start')}")

    if task.get('date_end'):
        lines.append(f"   End date: {task.get('date_end')}")

    if task.get('note_public'):
        lines.append(f"   Public note: {task.get('note_public')}")

    if task.get('note_private'):
        lines.append(f"   Private note: {task.get('note_private')}")

    return "\n".join(lines)

# === MCP TOOLS ===

@mcp.tool()
async def dolibarr_get_task(task_id: int, includetimespent: int = 0) -> str:
    """Get details of a specific Dolibarr task by ID with optional time spent data."""
    logger.info(f"Fetching task with ID: {task_id}")

    if not task_id or task_id <= 0:
        return "❌ Error: task_id is required and must be a positive integer"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        if includetimespent not in [0, 1, 2]:
            return "❌ Error: includetimespent must be 0, 1, or 2"

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/tasks/{task_id}"
            params = {"includetimespent": includetimespent}

            response = await client.get(url, headers=get_headers(), params=params, timeout=10)
            response.raise_for_status()
            task = response.json()

            result = f"✅ Task Retrieved:\n\n{format_task_info(task)}"

            # Add time spent information if requested
            if includetimespent >= 1 and task.get('timespent_total_duration'):
                hours = int(task.get('timespent_total_duration', 0)) / 3600
                result += f"\n\n⏱️  Time Spent Summary:"
                result += f"\n   Total duration: {hours:.2f} hours"
                result += f"\n   Number of entries: {task.get('timespent_nblines', 0)}"

                if task.get('timespent_min_date'):
                    result += f"\n   First entry: {task.get('timespent_min_date')}"
                if task.get('timespent_max_date'):
                    result += f"\n   Last entry: {task.get('timespent_max_date')}"

            # Add detailed time spent lines if requested
            if includetimespent == 2 and task.get('timespent_lines'):
                result += f"\n\n📊 Time Spent Entries:"
                for line in task.get('timespent_lines', []):
                    hours = int(line.get('task_duration', 0)) / 3600
                    result += f"\n   • ID {line.get('id')}: {hours:.2f}h on {line.get('task_date')}"
                    if line.get('note'):
                        result += f" - {line.get('note')}"

            return result

    except ValueError as e:
        return f"❌ Error: Invalid number format - {str(e)}"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Error: Task {task_id} not found"
        elif e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error fetching task: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_create_task(ref: str = "", label: str = "", fk_project: str = "", description: str = "", fk_task_parent: str = "", date_start: str = "", date_end: str = "", planned_workload: str = "", progress: str = "", priority: str = "", budget_amount: str = "", note_public: str = "", note_private: str = "") -> str:
    """Create a new Dolibarr task with required ref, label, and project ID."""
    logger.info(f"Creating task: {ref} - {label}")

    if not ref.strip():
        return "❌ Error: ref (task reference) is required"

    if not label.strip():
        return "❌ Error: label is required"

    if not fk_project.strip():
        return "❌ Error: fk_project (project ID) is required"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        task_data = {
            "ref": ref.strip(),
            "label": label.strip(),
            "fk_project": int(fk_project)
        }

        if description.strip():
            task_data["description"] = description.strip()

        if fk_task_parent.strip():
            try:
                task_data["fk_task_parent"] = int(fk_task_parent)
            except ValueError:
                return f"❌ Error: fk_task_parent must be a valid integer, got: {fk_task_parent}"

        if date_start.strip():
            try:
                task_data["date_start"] = int(date_start)
            except ValueError:
                return f"❌ Error: date_start must be a valid Unix timestamp (integer), got: {date_start}"

        if date_end.strip():
            try:
                task_data["date_end"] = int(date_end)
            except ValueError:
                return f"❌ Error: date_end must be a valid Unix timestamp (integer), got: {date_end}"

        if planned_workload.strip():
            try:
                # Convert hours to seconds
                hours = float(planned_workload)
                task_data["planned_workload"] = int(hours * 3600)
            except ValueError:
                return f"❌ Error: planned_workload must be a valid number (hours), got: {planned_workload}"

        if progress.strip():
            try:
                prog_int = int(progress)
                if 0 <= prog_int <= 100:
                    task_data["progress"] = prog_int
                else:
                    return "❌ Error: progress must be between 0 and 100"
            except ValueError:
                return f"❌ Error: progress must be a valid integer, got: {progress}"

        if priority.strip():
            try:
                task_data["priority"] = int(priority)
            except ValueError:
                return f"❌ Error: priority must be a valid integer, got: {priority}"

        if budget_amount.strip():
            try:
                task_data["budget_amount"] = float(budget_amount)
            except ValueError:
                return f"❌ Error: budget_amount must be a valid number, got: {budget_amount}"

        if note_public.strip():
            task_data["note_public"] = note_public.strip()

        if note_private.strip():
            task_data["note_private"] = note_private.strip()

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/tasks"
            response = await client.post(url, headers=get_headers(), json=task_data, timeout=10)
            response.raise_for_status()
            task_id = response.json()

            return f"✅ Task Created Successfully!\n\n   Task ID: {task_id}\n   Reference: {ref}\n   Label: {label}\n   Project ID: {fk_project}"

    except ValueError as e:
        return f"❌ Error: Invalid number format - {str(e)}"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        elif e.response.status_code == 400:
            return f"❌ Error: Invalid request - {e.response.text}"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_modify_task(task_id: int, label: str = "", description: str = "", progress: str = "", planned_workload: str = "", priority: str = "", budget_amount: str = "", date_start: str = "", date_end: str = "", note_public: str = "", note_private: str = "") -> str:
    """Update an existing Dolibarr task by ID."""
    logger.info(f"Updating task: {task_id}")

    if not task_id or task_id <= 0:
        return "❌ Error: task_id is required and must be a positive integer"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    update_data = {}

    if label.strip():
        update_data["label"] = label.strip()

    if description.strip():
        update_data["description"] = description.strip()

    if progress.strip():
        try:
            prog_int = int(progress)
            if 0 <= prog_int <= 100:
                update_data["progress"] = prog_int
            else:
                return "❌ Error: progress must be between 0 and 100"
        except ValueError:
            return f"❌ Error: progress must be a valid integer, got: {progress}"

    if planned_workload.strip():
        try:
            # Convert hours to seconds
            hours = float(planned_workload)
            update_data["planned_workload"] = int(hours * 3600)
        except ValueError:
            return f"❌ Error: planned_workload must be a valid number (hours), got: {planned_workload}"

    if priority.strip():
        try:
            update_data["priority"] = int(priority)
        except ValueError:
            return f"❌ Error: priority must be a valid integer, got: {priority}"

    if budget_amount.strip():
        try:
            update_data["budget_amount"] = float(budget_amount)
        except ValueError:
            return f"❌ Error: budget_amount must be a valid number, got: {budget_amount}"

    if date_start.strip():
        try:
            update_data["date_start"] = int(date_start)
        except ValueError:
            return f"❌ Error: date_start must be a valid Unix timestamp (integer), got: {date_start}"

    if date_end.strip():
        try:
            update_data["date_end"] = int(date_end)
        except ValueError:
            return f"❌ Error: date_end must be a valid Unix timestamp (integer), got: {date_end}"

    if note_public.strip():
        update_data["note_public"] = note_public.strip()

    if note_private.strip():
        update_data["note_private"] = note_private.strip()

    if not update_data:
        return "❌ Error: At least one field to update must be provided"

    try:
        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/tasks/{task_id}"
            response = await client.put(url, headers=get_headers(), json=update_data, timeout=10)
            response.raise_for_status()
            updated_task = response.json()

            return f"✅ Task Updated Successfully:\n\n{format_task_info(updated_task)}"

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Error: Task {task_id} not found"
        elif e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_task_add_spenttime(task_id: int, date: str = "", duration: str = "", user_id: str = "", note: str = "") -> str:
    """Add a time spent entry to a Dolibarr task."""
    logger.info(f"Adding time spent to task: {task_id}")

    if not task_id or task_id <= 0:
        return "❌ Error: task_id is required and must be a positive integer"

    if not date.strip():
        return "❌ Error: date is required (format: YYYY-MM-DD HH:MM:SS, YYYY-MM-DD, or YYYYMMDD)"

    if not duration.strip():
        return "❌ Error: duration is required (in hours, e.g., '2.5')"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        # Convert duration from hours to seconds
        duration_hours = float(duration)
        duration_seconds = int(duration_hours * 3600)

        # Convert date to required format (YYYY-MM-DD HH:MM:SS)
        date_str = date.strip()
        if len(date_str) == 10:  # Format: YYYY-MM-DD (no time component)
            date_str = f"{date_str} 12:00:00"
        elif len(date_str) == 8:  # Format: YYYYMMDD
            # Convert YYYYMMDD to YYYY-MM-DD HH:MM:SS
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} 12:00:00"
        # If date already has time component (19 chars), use as-is

        timespent_data = {
            "date": date_str,
            "duration": duration_seconds
        }

        if user_id.strip():
            try:
                timespent_data["user_id"] = int(user_id)
            except ValueError:
                return f"❌ Error: user_id must be a valid integer, got: {user_id}"

        if note.strip():
            timespent_data["note"] = note.strip()

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/tasks/{task_id}/addtimespent"
            response = await client.post(url, headers=get_headers(), json=timespent_data, timeout=10)
            response.raise_for_status()
            result = response.json()

            return f"✅ Time Spent Added Successfully!\n\n   Task ID: {task_id}\n   Date: {date_str}\n   Duration: {duration_hours} hours ({duration_seconds} seconds)\n   Note: {note if note else 'N/A'}"

    except ValueError as e:
        return f"❌ Error: Invalid number format - {str(e)}"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Error: Task {task_id} not found"
        elif e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        elif e.response.status_code == 400:
            return f"❌ Error: Invalid request - {e.response.text}"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error adding time spent: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting Dolibarr Tasks MCP server...")

    if not DOLIBARR_URL:
        logger.warning("DOLIBARR_URL not set - server will return errors until configured")
    if not DOLIBARR_API_KEY:
        logger.warning("DOLIBARR_API_KEY not set - server will return errors until configured")

    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
