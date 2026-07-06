"""
Google Workspace Assistant - Main Agent Definition

Part 1: Implement tools and system instruction for Calendar OR Tasks
Part 2: Add McpToolset for GitHub integration
"""

from config.settings import Settings
from google.adk.agents import LlmAgent
from tools.calendar_tools import calendar_tools
from tools.mcp_tools import get_github_mcp_toolset


def create_agent() -> LlmAgent:
    """Create the Workspace Assistant agent."""
    settings = Settings()

    try:
        github_toolset = get_github_mcp_toolset()
    except Exception as exc:
        github_toolset = None
        github_status = f"GitHub MCP is currently unavailable: {exc}"
    else:
        github_status = "GitHub MCP is available for repository and issue queries."

    instruction = f"""You are a helpful Google Workspace assistant for calendar management and GitHub workflows.
    Help the user list upcoming events, find available meeting slots, create calendar events,
    and check whether a proposed time conflicts with existing commitments. When available, also help
    with GitHub tasks such as listing repositories, inspecting issues, and creating issues.
    Be concise, clear, and confirm important details before creating or changing appointments.
    If a tool returns an error, explain it in plain language and suggest the next step.
    {github_status}
    """

    tools = list(calendar_tools)
    if github_toolset is not None:
        tools.append(github_toolset)

    return LlmAgent(
        name="workspace_assistant",
        model=settings.model_name,
        instruction=instruction,
        tools=tools,
    )


def create_agent_with_tool_search() -> LlmAgent:
    """BONUS: Create agent with defer_loading for tool search."""
    raise NotImplementedError("Bonus: Implement tool search pattern")
