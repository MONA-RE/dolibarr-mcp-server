# Bug Fix: Duration Double Conversion (CRITICAL)

## Date: 2025-12-20

## Problem

The `dolibarr_task_add_spenttime` function was performing a double conversion of duration values, resulting in time tracking data being multiplied by 3600.

### Root Cause

**Original Implementation**:
- MCP server API contract stated duration should be in **hours**
- AI agents (like N8N) were converting hours to **seconds** before sending to MCP server
- MCP server then converted these seconds again by multiplying by 3600
- Result: User requests "2 hours" → AI sends 7200 seconds → Server stores 25,920,000 seconds (7200 hours!)

### Example of Bug

**User Request**: "Add 2 hours of work on task 39"

**Flow**:
1. User says: "2 hours"
2. AI agent converts: 2 × 3600 = 7200 seconds
3. AI sends to MCP: `{"duration": "7200"}`
4. MCP server interprets as hours: 7200 hours
5. MCP server converts: 7200 × 3600 = 25,920,000 seconds
6. **Stored in DB**: 25,920,000 seconds = 7200 hours ❌

**Expected**: 7200 seconds = 2 hours ✅

### Impact

- **CRITICAL**: All time spent entries had durations multiplied by 3600
- Time tracking data completely incorrect
- Project reporting and billing affected
- Feature unusable in production

---

## Solution: Option A - Accept Seconds Directly

Changed the MCP server to accept duration in **seconds** directly, eliminating the double conversion.

### Code Changes

**File**: `mcp-server-tasks/dolibarr_tasks_server.py`

#### Change 1: Updated Docstring (Line 341)
```python
# Before:
"""Add a time spent entry to a Dolibarr task."""

# After:
"""Add a time spent entry to a Dolibarr task (duration in seconds)."""
```

#### Change 2: Updated Error Message (Line 351)
```python
# Before:
return "❌ Error: duration is required (in hours, e.g., '2.5')"

# After:
return "❌ Error: duration is required (in seconds, e.g., '7200' for 2 hours)"
```

#### Change 3: Removed Conversion, Accept Seconds (Lines 357-359)
```python
# Before:
# Convert duration from hours to seconds
duration_hours = float(duration)
duration_seconds = int(duration_hours * 3600)

# After:
# Accept duration in seconds (no conversion needed)
duration_seconds = int(float(duration))
duration_hours = round(duration_seconds / 3600, 2)
```

#### Change 4: Updated Success Message (Line 411)
```python
# Before:
return f"✅ Time Spent Added Successfully!\n\n   Task ID: {task_id}\n   Date: {date_str}\n   Duration: {duration_hours} hours ({duration_seconds} seconds)\n   Note: {note if note else 'N/A'}"

# After:
return f"✅ Time Spent Added Successfully!\n\n   Task ID: {task_id}\n   Date: {date_str}\n   Duration: {duration_seconds} seconds ({duration_hours} hours)\n   Note: {note if note else 'N/A'}"
```

### Documentation Changes

**File**: `mcp-server-tasks/CLAUDE.md`

#### Update 1: Duration Conversion Section (Lines 167-171)
```markdown
# Before:
### Duration Conversion
- Input: Hours (decimal, e.g., "2.5" = 2h30m)
- Storage: Seconds (integer, e.g., 9000)
- Conversion: `seconds = int(hours * 3600)`
- Display: `hours = seconds / 3600`

# After:
### Duration Conversion
- Input: Seconds (integer, e.g., "7200" = 2 hours)
- Storage: Seconds (integer, e.g., 7200)
- Conversion: No conversion needed (direct pass-through)
- Display: `hours = seconds / 3600`
```

#### Update 2: Tool Parameters (Line 223)
```markdown
# Before:
- `duration` (required): Duration in hours (e.g., "2.5")

# After:
- `duration` (required): Duration in seconds (e.g., "7200" for 2 hours, "3600" for 1 hour)
```

#### Update 3: Time/Duration Helper Note (Line 254)
```markdown
# Added:
**Note**: The MCP server now accepts duration in **seconds** directly. Clients (AI agents, applications) should convert hours to seconds before sending to the MCP server using the helpers below.
```

---

## Deployment

### Steps Executed

1. ✅ Updated `dolibarr_tasks_server.py`
2. ✅ Updated `CLAUDE.md` documentation
3. ✅ Rebuilt Docker image:
   ```bash
   cd /home/teddy/docker-workspace/dolibarr-mcp-server/mcp-gateway-standalone
   docker compose --profile build-only build dolibarr-tasks
   ```
4. ✅ Restarted MCP Gateway:
   ```bash
   docker compose restart gateway
   ```

### Build Output
```
#12 exporting to image
#12 exporting layers 0.0s done
#12 exporting manifest sha256:6ec7c38f4090267d5da9e8b6719676bb1a0e860cce33f1310b27404898ac1303 done
#12 naming to docker.io/library/dolibarr-tasks-mcp-server:latest done
#12 DONE 0.1s

dolibarr-tasks-mcp-server:latest  Built
```

### Gateway Restart
```
Container mcp_dolibarr  Restarting
Container mcp_dolibarr  Started
```

---

## Testing

### Test Case 1: Add 3 Hours to Task 39

**Request**:
```bash
curl -X POST http://localhost:5678/webhook/webhook_message \
  -H "Content-Type:application/json" \
  -d '{"message": "Ajoute 3 heures de travail sur la tâche 39 pour le 21 décembre 2025"}'
```

**Agent Response**:
```
✅ Time Spent Added Successfully!

   Task ID: 39
   Date: 2025-12-21 12:00:00
   Duration: 10800 seconds (3.0 hours)
   Note: N/A
```

**Database Verification**:
```sql
SELECT rowid, fk_task, task_date, task_duration,
       ROUND(task_duration / 3600, 2) as hours, note
FROM llx_projet_task_time
WHERE rowid = 6;
```

**Result**:
```
rowid: 6
fk_task: 39
task_date: 2025-12-21
task_duration: 10800
hours: 3.00
note: NULL
```

**Status**: ✅ **PASS** - Exactly 3 hours stored correctly!

---

### Test Case 2: Add 1.5 Hours to Task 38 with Note

**Request**:
```bash
curl -X POST http://localhost:5678/webhook/webhook_message \
  -H "Content-Type:application/json" \
  -d '{"message": "Ajoute 1.5 heures sur la tâche 38 pour aujourd'"'"'hui avec la note \"Correction de bug\""}'
```

**Agent Response**:
```
✅ Time Spent Added Successfully!

   Task ID: 38
   Date: 2025-12-20 12:00:00
   Duration: 5400 seconds (1.5 hours)
   Note: Correction de bug
```

**Database Verification**:
```sql
SELECT rowid, fk_task, task_date, task_duration,
       ROUND(task_duration / 3600, 2) as hours, note
FROM llx_projet_task_time
WHERE rowid = 7;
```

**Result**:
```
rowid: 7
fk_task: 38
task_date: 2025-12-20
task_duration: 5400
hours: 1.50
note: Correction de bug
```

**Status**: ✅ **PASS** - Exactly 1.5 hours with note stored correctly!

---

### Comparison: Before vs After Fix

**Task 39 Entries**:
```
rowid   task_date   task_duration   hours      Status
5       2025-12-20  25920000        7200.00    ❌ BEFORE FIX (bug - double conversion)
6       2025-12-21  10800           3.00       ✅ AFTER FIX (correct)
```

**Analysis**:
- Old entry (rowid 5): Shows the bug - 7200 hours instead of 2 hours
- New entry (rowid 6): Correct - exactly 3 hours as requested

---

## Impact Analysis

### Before Fix
- ❌ Time tracking completely broken
- ❌ All durations multiplied by 3600
- ❌ Example: User enters 2 hours → System stores 7200 hours
- ❌ Feature unusable in production
- ❌ Data integrity compromised

### After Fix
- ✅ Time tracking works correctly
- ✅ Durations stored accurately
- ✅ Example: User enters 2 hours → System stores 2 hours (7200 seconds)
- ✅ Feature ready for production
- ✅ Data integrity maintained

---

## Backward Compatibility

### Breaking Change
⚠️ **This is a breaking change** for any client code that was working around the bug.

**Impact**:
- Clients must now send duration in **seconds** (not hours)
- AI agents are already doing this correctly (no change needed for N8N)
- Direct API calls must be updated

**Migration Guide**:
```python
# Old code (was sending hours, but bug made it work):
# DON'T DO THIS ANYMORE
duration = "2"  # This would be stored as 2 seconds now (incorrect)

# New code (correct):
duration_hours = 2
duration_seconds = duration_hours * 3600  # 7200
duration = str(duration_seconds)  # "7200"
```

### Data Cleanup

Existing incorrect data in database should be reviewed:
```sql
-- Find entries with suspiciously large durations (> 100 hours = 360000 seconds)
SELECT rowid, fk_task, task_date, task_duration,
       ROUND(task_duration / 3600, 2) as hours
FROM llx_projet_task_time
WHERE task_duration > 360000
ORDER BY task_duration DESC;
```

**Action Items**:
1. Review and correct historical data affected by the bug
2. Notify users of the fix
3. Update any client applications

---

## Why Option A Was Chosen

### Options Considered

**Option A**: Accept seconds directly (CHOSEN) ✅
- Pros: Simple, consistent with Dolibarr API, no ambiguity
- Cons: Breaking change

**Option B**: Intelligent detection (hours vs seconds)
- Pros: Could handle both formats
- Cons: Complex, ambiguous (what if someone works 100+ hours?), error-prone

**Option C**: Add explicit unit parameter
- Pros: Clear intent
- Cons: More complex API, breaking change anyway

### Rationale for Option A

1. **Consistency**: Dolibarr API uses seconds internally
2. **Simplicity**: No conversion logic needed in MCP server
3. **Clarity**: Explicit about expected unit
4. **AI-Friendly**: AI agents already convert to seconds
5. **No Ambiguity**: 7200 seconds is always 2 hours, no guessing

---

## Lessons Learned

### API Design
- Document expected units clearly in function signatures
- Validate assumptions about client behavior
- Test with real clients (not just unit tests)

### Testing
- Integration tests should verify database state
- Test with actual AI agents to catch conversion issues
- Cross-reference API responses with database

### Documentation
- Keep code comments and documentation in sync
- Document units explicitly (seconds vs hours vs milliseconds)
- Provide examples with actual values

---

## Related Issues

### To Be Fixed

1. **ISO 8601 Date Support** (Bug #2)
   - File: `mcp-server-tasks/dolibarr_tasks_server.py`
   - Issue: Dates like `2025-12-20T05:00:00-05:00` cause 400 errors
   - Priority: HIGH

### Future Enhancements

1. Add data validation for duration (max hours per entry)
2. Add historical data cleanup script
3. Add automated regression tests
4. Consider adding timezone support for dates

---

## Files Modified

1. `/mcp-server-tasks/dolibarr_tasks_server.py` - Core implementation
2. `/mcp-server-tasks/CLAUDE.md` - Documentation
3. `/mcp-server-tasks/BUGFIX_DURATION_DOUBLE_CONVERSION.md` - This file

---

## References

- Original bug report: `test-task/ai_agent_test_instructions_task_results2.md`
- Test execution date: 2025-12-20
- Docker image rebuilt: `dolibarr-tasks-mcp-server:latest`
- Gateway container: `mcp_dolibarr`

---

**Fix Status**: ✅ **COMPLETE AND VERIFIED**

**Production Ready**: ✅ **YES** (with data cleanup recommended)

**Report Generated**: 2025-12-20
**Fixed By**: Claude Code AI Agent
**Verified**: Database and N8N integration tests passed
