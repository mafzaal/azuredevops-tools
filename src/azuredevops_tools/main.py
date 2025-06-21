"""
Main entry point for the Azure DevOps Tools MCP server.
"""

from .tools import (
    get_build_logs_tool, 
    get_build_log_full_content_tool, 
    get_build_tool, 
    get_builds_tool, 
    get_changeset_tool, 
    get_changeset_changes_tool, 
    get_file_diff_tool, 
    get_changeset_list_tool, 
    get_failed_tasks_with_logs_tool, 
    get_build_pipelines_tool
)
from mcp.server.fastmcp import FastMCP


def create_mcp_server():
    """Create and configure the MCP server with all available tools."""
    # Initialize FastMCP server
    mcp = FastMCP("devops_tools", description="DevOps Tools for Azure DevOps", version="0.1.0")
    
    # Add changeset tools
    mcp.add_tool(get_changeset_tool)
    mcp.add_tool(get_changeset_changes_tool)
    mcp.add_tool(get_changeset_list_tool)
    mcp.add_tool(get_file_diff_tool)
    
    # Add build tools
    mcp.add_tool(get_build_tool)
    mcp.add_tool(get_builds_tool)
    mcp.add_tool(get_build_logs_tool)
    mcp.add_tool(get_build_log_full_content_tool)
    mcp.add_tool(get_failed_tasks_with_logs_tool)
    mcp.add_tool(get_build_pipelines_tool)
    
    return mcp


def main():
    """Main entry point for the MCP server."""
    mcp = create_mcp_server()
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
