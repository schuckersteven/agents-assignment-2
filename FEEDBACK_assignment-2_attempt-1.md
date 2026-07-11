## Grade: 91 / 100

**Assignment:** Google Workspace Assistant + GitHub MCP (ADK)  
**Attempt:** 1 of 2  ·  **Graded:** 2026-07-11  ·  Commit `4b79314`

### Score breakdown
| Criterion | Max | Earned | Notes |
|-----------|-----|--------|-------|
| tool_design | 18 | 18 | Four calendar tools implemented as plain functions with clear, intent-revealing names (list_upcoming_events, find_available_slots, create_event, check_conflicts), complete Args/Returns docstrings, and typed parameters; all collected into the calendar_tools list (line 235). Exceeds the 3-tool requirement. (`workspace_assistant/tools/calendar_tools.py:26-240`) |
| agent_instructions | 14 | 12 | System instruction is clear and scoped, describes each capability, and includes safe-behavior guidance ('confirm important details before creating or changing appointments') plus error-explanation guidance. Could be strengthened with more explicit per-tool selection cues, but covers the essentials well. (`workspace_assistant/agent.py:26-33`) |
| error_handling | 14 | 13 | Every tool wraps its API calls in try/except and returns a consistent {status, message} dict on failure. Edge cases are validated up front (empty summary, non-positive duration, end<=start) and surface as friendly error dicts. Messages pass str(e) straight through; wrapping raw exception text in more user-facing phrasing would be the next step. (`workspace_assistant/tools/calendar_tools.py:48-49,126-127,173-174,231-232`) |
| functionality | 14 | 13 | Tools call the correct Calendar API through get_calendar_service() (events().list / events().insert) and the intended logic is statically correct: the free/busy overlap test (current < busy_end and slot_end > busy_start) and the conflict test are both sound. Handles all-day (date) and timed (dateTime) events. Judged statically; not executed. (`workspace_assistant/tools/calendar_tools.py:36-46,158-171,109-123,223`) |
| code_quality | 10 | 9 | Readable and well organized: a shared _parse_datetime helper avoids duplication, docstrings are thorough, and the tools are wired into an LlmAgent via create_agent(). Minor: return types are annotated only as dict rather than a structured type. (`workspace_assistant/tools/calendar_tools.py:13-23; workspace_assistant/agent.py:14-44`) |
| mcp_configured | 10 | 9 | McpToolset is configured correctly for the GitHub MCP server (StdioConnectionParams wrapping StdioServerParameters, npx @modelcontextprotocol/server-github, token injected via env) and attached to the agent in create_agent(). Note: the module-level mcp_tools list (line 149) is left empty, but the agent imports and calls get_github_mcp_toolset() directly, so wiring is functionally complete. (`workspace_assistant/tools/mcp_tools.py:28-42; workspace_assistant/agent.py:19-37`) |
| github_queries | 15 | 12 | GitHub queries route through the MCP toolset, which auto-exposes the server's repo/issue/PR tools; the toolset is appended to the agent's tool list and the instruction directs it toward listing repos, inspecting issues, and creating issues. The reflection documents obtaining a token with issue-write scope. Correct delegation-based design; no custom query wrappers, judged statically. (`workspace_assistant/agent.py:35-37,26-33; workspace_assistant/tools/mcp_tools.py:34-42`) |
| mcp_error_handling | 5 | 5 | Missing token raises a clear ValueError, and create_agent() wraps toolset creation in try/except, degrades gracefully to a None toolset, and injects a plain-language 'GitHub MCP is currently unavailable' status into the instruction so the agent still functions for calendar tasks. (`workspace_assistant/tools/mcp_tools.py:30-32; workspace_assistant/agent.py:18-24,32`) |
| Integrity deduction | — | 0 | Provided files unmodified |
| **Total** | **100** | **91** | |

### What went well
- Complete Option A implementation: four well-named calendar tools with thorough docstrings and typed parameters, cleanly collected into calendar_tools (calendar_tools.py:26-240).
- Consistent, defensive error handling across every tool with a uniform {status, message} contract plus up-front input validation (calendar_tools.py:66-69,150-156,191-192).
- Statically correct scheduling logic: the free-slot search and conflict detection both use a sound interval-overlap test and handle all-day vs. timed events (calendar_tools.py:109-123,223).
- GitHub MCP integration is wired correctly and degrades gracefully when the token or server is unavailable (agent.py:18-37, mcp_tools.py:30-42).

### What to improve (actionable)
- The bonus tool-search path is entirely unimplemented: create_agent_with_tool_search() raises NotImplementedError and defer_loading/search_github_tools remain commented examples (agent.py:47-49, mcp_tools.py:118-146).
- Error messages return raw str(e); wrapping them in more user-facing phrasing per failure mode would match the reflection's stated goal of conversational errors (calendar_tools.py:49,127).
- The module-level mcp_tools list is left empty (mcp_tools.py:149-153); populate it or remove it to avoid implying the toolset is unwired.
- The system instruction could give more explicit per-tool selection cues (when to prefer find_available_slots vs. check_conflicts) to sharpen tool routing (agent.py:26-33).

### Automated checks
- ✅ All required files implemented
- ✅ Provided files unmodified
- ✅ 0/0 output artifacts committed
- ✅ Reflection 444 words

### Resubmission
You may resubmit **once**. Push fixes to this repo, then notify the instructor; we'll re-grade as **Attempt 2 (final)**. This is attempt 1 of 2.

---
*Graded automatically with Claude Code against the course rubric. Questions → contact the instructor.*


---
<sub>🔎 **Autograder record** — attempt 1 of 2 · graded at commit `4b79314` · delivered 2026-07-11T18:20:19Z. Commits pushed to `main` after this timestamp are treated as a resubmission.</sub>
