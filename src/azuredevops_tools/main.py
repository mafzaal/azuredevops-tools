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
    get_build_pipelines_tool,
    # Project tools
    get_projects_tool,
    # Git repository tools
    get_git_repositories_tool,
    get_git_repository_tool,
    get_git_commits_tool,
    get_git_commit_details_tool,
    # Pull request tools
    get_pull_requests_tool,
    get_pull_request_details_tool,
    create_pull_request_tool,
    approve_pull_request_tool,
    reject_pull_request_tool,
    request_pull_request_changes_tool,
    get_pull_request_policies_tool
)
from mcp.server.fastmcp import FastMCP


def create_mcp_server():
    """Create and configure the MCP server with all available tools."""
    # Initialize FastMCP server
    mcp = FastMCP(name="devops_tools", instructions="Tools for interacting with Azure DevOps.")
    
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
    
    # Add project tools
    mcp.add_tool(get_projects_tool)
    
    # Add Git repository tools
    mcp.add_tool(get_git_repositories_tool)
    mcp.add_tool(get_git_repository_tool)
    mcp.add_tool(get_git_commits_tool)
    mcp.add_tool(get_git_commit_details_tool)
    
    # Add pull request tools
    mcp.add_tool(get_pull_requests_tool)
    mcp.add_tool(get_pull_request_details_tool)
    mcp.add_tool(create_pull_request_tool)
    mcp.add_tool(get_pull_request_policies_tool)
    
    # Add approval workflow tools
    mcp.add_tool(approve_pull_request_tool)
    mcp.add_tool(reject_pull_request_tool)
    mcp.add_tool(request_pull_request_changes_tool)
    
    return mcp


def main():
    """Main entry point for the MCP server."""
    mcp = create_mcp_server()
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
