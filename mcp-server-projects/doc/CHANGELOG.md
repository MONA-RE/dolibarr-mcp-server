# Changelog - Dolibarr MCP Projects Server

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-12-18

### Fixed

#### Bug 1: Critical fk_soc Field Mapping (HIGH PRIORITY 🔴)
- **Issue:** Projects created via MCP server couldn't be associated with a third party (client)
- **Root Cause:** Server was sending `fk_soc` field name but Dolibarr API expects `socid`
- **Fix:** Changed `project_data["fk_soc"]` to `project_data["socid"]` in `dolibarr_create_project()` (line 216)
- **Impact:** Projects can now be correctly linked to third parties/clients
- **Commit:** 971e467

#### Bug 2: Third Party ID Display (MEDIUM PRIORITY 🟡)
- **Issue:** Third Party ID was never displayed in project details responses
- **Root Cause:** Function checked only `fk_soc` field but API returns `socid`
- **Fix:** Updated `format_project_info()` to check both `socid` (API response) and `fk_soc` (direct database access)
- **Impact:** Third Party ID now displays correctly in all responses
- **Commit:** 971e467

### Added

#### Enhancement 1: Deletion Confirmation (Safety Feature 🔒)
- **Feature:** Added optional `confirm` parameter to `dolibarr_delete_project()`
- **Behavior:** Deletion now requires explicit `confirm='yes'` to proceed
- **Safety:** Displays warning message if confirmation not provided
- **Benefits:** Prevents accidental deletion of projects
- **Commit:** 7da469a

#### Enhancement 2: Search by Reference Code 🔍
- **Feature:** New function `dolibarr_get_project_by_ref(ref: str)`
- **Purpose:** Allows retrieving projects by reference (e.g., "PJ2512-0001") instead of numeric ID
- **Implementation:** Uses Dolibarr API's `sqlfilters` parameter
- **Benefits:** More intuitive for users who know the reference but not the ID
- **Commit:** 7da469a

#### Enhancement 3: Auto-Pagination for Complete Lists 📊
- **Feature:** New function `dolibarr_list_all_projects()`
- **Purpose:** Retrieves ALL projects automatically without manual pagination
- **Mechanism:** Internal loop fetching 100 projects per page
- **Benefits:** Single call to get complete project list, useful for reports/exports
- **Limitations:** May be slow for >1000 projects, higher memory usage
- **Commit:** 7da469a

### Changed

- Improved error messages and warning formatting
- Enhanced user feedback for deletion operations
- Better support for different API response formats

### Testing

- ✅ Bug 1: Verified project creation with `socid = 1` in database
- ✅ Bug 2: Verified Third Party ID display in project details
- ✅ Enhancement 1: Tested deletion confirmation mechanism
- ✅ Enhancement 2: Retrieved project by reference TEST-CORRECTION-001
- ✅ Enhancement 3: Retrieved all 6 projects with auto-pagination

---

## [1.0.0] - 2025-12-01

### Added

- Initial release of Dolibarr MCP Projects Server
- Complete CRUD operations for Dolibarr projects
- MCP tool: `dolibarr_get_project(project_id)` - Get project details by ID
- MCP tool: `dolibarr_list_projects()` - List projects with pagination
- MCP tool: `dolibarr_create_project()` - Create new project
- MCP tool: `dolibarr_update_project()` - Update existing project
- MCP tool: `dolibarr_delete_project()` - Delete project
- MCP tool: `dolibarr_get_project_tasks()` - Get tasks for a project
- Support for pagination (limit, page, sortfield, sortorder)
- URL generation for direct access to Dolibarr interface
- Status mapping (Brouillon, Validé, Fermé)
- Date formatting in dd/MM/YYYY format
- Comprehensive error handling and validation
- Docker containerization with Python 3.11
- FastMCP framework integration
- Async/await pattern for all API calls

### Technical Details

- Python 3.11-slim base image
- FastMCP server framework
- httpx for async HTTP requests
- Non-root user (mcpuser) for security
- Environment-based configuration (DOLIBARR_URL, DOLIBARR_API_KEY)

---

## Version History Summary

| Version | Date | Type | Description |
|---------|------|------|-------------|
| 1.1.0 | 2025-12-18 | Feature + Bugfix | Fixed 2 critical bugs, added 3 improvements |
| 1.0.0 | 2025-12-01 | Initial Release | Complete MCP server with CRUD operations |

---

## Migration Guide

### Migrating from 1.0.0 to 1.1.0

**Breaking Changes:**
- None. All changes are backward compatible.

**New Features to Adopt:**

1. **Use Search by Reference:**
   ```python
   # Old way (still works)
   dolibarr_get_project(project_id=123)

   # New way (more user-friendly)
   dolibarr_get_project_by_ref(ref="PJ2512-0001")
   ```

2. **Use Auto-Pagination:**
   ```python
   # Old way (manual pagination)
   dolibarr_list_projects(limit="100", page="0")
   dolibarr_list_projects(limit="100", page="1")
   # ... continue until less than 100 results

   # New way (automatic)
   dolibarr_list_all_projects()
   ```

3. **Deletion Confirmation:**
   ```python
   # Old behavior: immediate deletion
   dolibarr_delete_project(project_id=123)

   # New behavior: requires confirmation
   dolibarr_delete_project(project_id=123, confirm="yes")
   ```

**Bug Fixes Applied Automatically:**
- Projects with third party associations will now save correctly
- Third Party ID will display in project details

---

## Upcoming Features (Planned)

### Version 1.2.0 (Future)

**Potential Enhancements:**
- `dolibarr_validate_project()` - Validate draft projects (POST /projects/{id}/validate)
- `dolibarr_close_project()` - Close completed projects
- `dolibarr_get_project_roles()` - Get user roles for a project
- `dolibarr_filter_projects_by_category()` - Filter by category
- `dolibarr_filter_projects_by_thirdparty()` - Filter by client/third party
- `dolibarr_advanced_filter_projects()` - Advanced SQL filters
- Task management enhancements (create, update, delete tasks)
- Time tracking integration
- Project cloning functionality

**Documentation Improvements:**
- Interactive API examples
- Postman collection
- Integration guides for popular platforms
- Video tutorials

---

## Support & Contributing

**Issues:** Report bugs or request features at the project repository

**Testing:** All changes are tested against a live Dolibarr instance

**Standards:** Follows MCP Server Constraints (see CLAUDE.md)

---

## Credits

**Generated with:** Claude Code (https://claude.com/claude-code)

**Development Team:**
- Claude Sonnet 4.5 <noreply@anthropic.com>

**Framework:** FastMCP (Model Context Protocol)

**API:** Dolibarr ERP/CRM REST API

---

*Last Updated: 2025-12-18*
