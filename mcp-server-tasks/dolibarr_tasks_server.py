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

def convert_iso_date_to_timestamp(date_str: str) -> int:
    """
    Convert ISO 8601 date to Unix timestamp.

    Accepts:
    - Full ISO 8601: YYYY-MM-DDTHH:MM:SS (e.g., "2025-12-22T14:30:00")
    - Simple date: YYYY-MM-DD (e.g., "2025-12-22") - will be set to midnight (00:00:00)

    Returns: Unix timestamp (integer) for Dolibarr API

    Raises: ValueError if date format is invalid
    """
    date_str = date_str.strip()

    # Case 1: Full ISO 8601 format with time (YYYY-MM-DDTHH:MM:SS)
    if "T" in date_str:
        # Parse ISO 8601 format
        try:
            dt = datetime.fromisoformat(date_str)
            # Convert to UTC timestamp
            return int(dt.replace(tzinfo=timezone.utc).timestamp())
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 date format. Expected YYYY-MM-DDTHH:MM:SS, got: {date_str}")

    # Case 2: Simple date format (YYYY-MM-DD) - set to midnight
    elif len(date_str) == 10 and date_str.count("-") == 2:
        try:
            # Add midnight time (00:00:00)
            dt = datetime.fromisoformat(f"{date_str}T00:00:00")
            # Convert to UTC timestamp
            return int(dt.replace(tzinfo=timezone.utc).timestamp())
        except ValueError:
            raise ValueError(f"Invalid date format. Expected YYYY-MM-DD, got: {date_str}")

    else:
        raise ValueError(f"Invalid date format. Expected YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD, got: {date_str}")

def convert_iso_date_to_dolibarr_format(date_str: str) -> str:
    """
    Convert ISO 8601 date to Dolibarr format (YYYY-MM-DD HH:MM:SS).

    Accepts:
    - Full ISO 8601: YYYY-MM-DDTHH:MM:SS (e.g., "2025-12-22T14:30:00")
    - Simple date: YYYY-MM-DD (e.g., "2025-12-22") - will be set to midnight (00:00:00)

    Returns: Date string in format "YYYY-MM-DD HH:MM:SS" for Dolibarr API

    Raises: ValueError if date format is invalid
    """
    date_str = date_str.strip()

    # Case 1: Full ISO 8601 format with time (YYYY-MM-DDTHH:MM:SS)
    if "T" in date_str:
        # Parse ISO 8601 format and convert to YYYY-MM-DD HH:MM:SS
        try:
            dt = datetime.fromisoformat(date_str)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 date format. Expected YYYY-MM-DDTHH:MM:SS, got: {date_str}")

    # Case 2: Simple date format (YYYY-MM-DD) - set to midnight
    elif len(date_str) == 10 and date_str.count("-") == 2:
        try:
            # Validate the date format
            datetime.fromisoformat(date_str)
            # Return with midnight time (00:00:00)
            return f"{date_str} 00:00:00"
        except ValueError:
            raise ValueError(f"Invalid date format. Expected YYYY-MM-DD, got: {date_str}")

    else:
        raise ValueError(f"Invalid date format. Expected YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD, got: {date_str}")

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
async def dolibarr_list_tasks(sortfield: str = "t.rowid", sortorder: str = "ASC", limit: str = "100", page: str = "0", sqlfilters: str = "") -> str:
    """List Dolibarr tasks with pagination and filtering options."""
    logger.info(f"Listing tasks with limit={limit}, page={page}, sortfield={sortfield}")

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        # Validate and convert parameters
        limit_int = int(limit) if limit.strip() else 100
        page_int = int(page) if page.strip() else 0

        if limit_int < 0 or limit_int > 1000:
            return "❌ Error: limit must be between 0 and 1000"

        if page_int < 0:
            return "❌ Error: page must be >= 0"

        params = {
            "sortfield": sortfield if sortfield.strip() else "t.rowid",
            "sortorder": sortorder if sortorder.strip() else "ASC",
            "limit": str(limit_int),
            "page": str(page_int)
        }

        if sqlfilters.strip():
            params["sqlfilters"] = sqlfilters.strip()

        async with httpx.AsyncClient() as client:
            url = f"{DOLIBARR_URL}/api/index.php/tasks"
            response = await client.get(url, headers=get_headers(), params=params, timeout=30)
            response.raise_for_status()
            tasks = response.json()

            if not tasks or len(tasks) == 0:
                return "ℹ️  No tasks found"

            result = f"✅ Tasks Retrieved: {len(tasks)} task(s)\n"
            result += f"   Page: {page_int} | Limit: {limit_int} | Sort: {params['sortfield']} {params['sortorder']}\n\n"

            for task in tasks:
                result += f"📋 {task.get('label', 'N/A')}\n"
                result += f"   ID: {task.get('id', 'N/A')} | Ref: {task.get('ref', 'N/A')}\n"
                result += f"   Project ID: {task.get('fk_project', 'N/A')}\n"

                if task.get('progress') is not None:
                    result += f"   Progress: {task.get('progress')}%\n"

                if task.get('planned_workload'):
                    hours = int(task.get('planned_workload')) / 3600
                    result += f"   Planned: {hours:.2f}h\n"

                if task.get('date_start'):
                    result += f"   Start: {task.get('date_start')}\n"

                if task.get('date_end'):
                    result += f"   End: {task.get('date_end')}\n"

                result += "\n"

            # Add pagination info
            if len(tasks) == limit_int:
                result += f"💡 Tip: There may be more tasks. Use page={page_int + 1} to see the next page.\n"

            return result

    except ValueError as e:
        return f"❌ Error: Invalid number format - {str(e)}"
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "❌ Error: Authentication failed or insufficient permissions"
        else:
            return f"❌ API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def dolibarr_create_task(ref: str = "", label: str = "", fk_project: str = "", description: str = "", fk_task_parent: str = "", date_start: str = "", date_end: str = "", planned_workload: str = "", progress: str = "", priority: str = "", budget_amount: str = "", note_public: str = "", note_private: str = "") -> str:
    """Create a new Dolibarr task - planned_workload in SECONDS, date_start/date_end in ISO 8601 format (YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD)."""
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

        # Date format: ISO 8601 (YYYY-MM-DDTHH:MM:SS) or simple date (YYYY-MM-DD)
        if date_start.strip():
            try:
                task_data["date_start"] = convert_iso_date_to_timestamp(date_start)
            except ValueError as e:
                return f"❌ Error: date_start - {str(e)}"

        if date_end.strip():
            try:
                task_data["date_end"] = convert_iso_date_to_timestamp(date_end)
            except ValueError as e:
                return f"❌ Error: date_end - {str(e)}"

        if planned_workload.strip():
            try:
                # planned_workload must be in SECONDS (not hours)
                seconds = int(float(planned_workload))

                # Validation: warn if value seems too small (likely hours instead of seconds)
                if seconds > 0 and seconds < 3600:
                    logger.warning(f"planned_workload={seconds}s is less than 1 hour - did you mean to send seconds?")
                    return f"❌ Error: planned_workload must be in SECONDS, not hours. Got {seconds} which is only {seconds/60:.1f} minutes. For 20 hours, send '72000' (20*3600). For 1 hour, send '3600'."

                task_data["planned_workload"] = seconds
            except ValueError:
                return f"❌ Error: planned_workload must be a valid number in SECONDS (e.g., '72000' for 20 hours), got: {planned_workload}"

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
    """Update an existing Dolibarr task - planned_workload in SECONDS, date_start/date_end in ISO 8601 format (YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD)."""
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
            # planned_workload must be in SECONDS (not hours)
            seconds = int(float(planned_workload))

            # Validation: warn if value seems too small (likely hours instead of seconds)
            if seconds > 0 and seconds < 3600:
                logger.warning(f"planned_workload={seconds}s is less than 1 hour - did you mean to send seconds?")
                return f"❌ Error: planned_workload must be in SECONDS, not hours. Got {seconds} which is only {seconds/60:.1f} minutes. For 20 hours, send '72000' (20*3600). For 1 hour, send '3600'."

            update_data["planned_workload"] = seconds
        except ValueError:
            return f"❌ Error: planned_workload must be a valid number in SECONDS (e.g., '72000' for 20 hours), got: {planned_workload}"

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

    # Date format: ISO 8601 (YYYY-MM-DDTHH:MM:SS) or simple date (YYYY-MM-DD)
    if date_start.strip():
        try:
            update_data["date_start"] = convert_iso_date_to_timestamp(date_start)
        except ValueError as e:
            return f"❌ Error: date_start - {str(e)}"

    if date_end.strip():
        try:
            update_data["date_end"] = convert_iso_date_to_timestamp(date_end)
        except ValueError as e:
            return f"❌ Error: date_end - {str(e)}"

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
    """Add a time spent entry to a Dolibarr task - date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD), duration in seconds."""
    logger.info(f"Adding time spent to task: {task_id}")

    if not task_id or task_id <= 0:
        return "❌ Error: task_id is required and must be a positive integer"

    if not date.strip():
        return "❌ Error: date is required (format: ISO 8601 - YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD)"

    if not duration.strip():
        return "❌ Error: duration is required (in seconds, e.g., '7200' for 2 hours)"

    if not DOLIBARR_URL or not DOLIBARR_API_KEY:
        return "❌ Error: DOLIBARR_URL and DOLIBARR_API_KEY must be configured"

    try:
        # Accept duration in seconds (no conversion needed)
        duration_seconds = int(float(duration))
        duration_hours = round(duration_seconds / 3600, 2)

        # Convert date to Dolibarr format (YYYY-MM-DD HH:MM:SS)
        # Accepts ISO 8601: YYYY-MM-DDTHH:MM:SS or simple date: YYYY-MM-DD
        try:
            date_str = convert_iso_date_to_dolibarr_format(date)
        except ValueError as e:
            return f"❌ Error: date - {str(e)}"

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

            return f"✅ Time Spent Added Successfully!\n\n   Task ID: {task_id}\n   Date: {date_str}\n   Duration: {duration_seconds} seconds ({duration_hours} hours)\n   Note: {note if note else 'N/A'}"

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
