
from tools import get_build_logs_tool, get_build_log_full_content_tool, get_build_tool, get_builds_tool, get_changeset_tool, get_changeset_changes_tool, get_file_diff_tool, get_changeset_list_tool, get_failed_tasks_with_logs_tool, get_build_pipelines_tool
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("devops_tools", description="DevOps Tools for Azure DevOps", version="0.1.0")

def main():
    pass

    mcp.add_tool(get_changeset_tool)
    mcp.add_tool(get_changeset_changes_tool)
    mcp.add_tool(get_changeset_list_tool)
    mcp.add_tool(get_file_diff_tool)
    
    mcp.add_tool(get_build_tool)
    mcp.add_tool(get_builds_tool)
    mcp.add_tool(get_build_logs_tool)
    mcp.add_tool(get_build_log_full_content_tool)
    mcp.add_tool(get_failed_tasks_with_logs_tool)
    mcp.add_tool(get_build_pipelines_tool)
    mcp.run(transport='stdio')
    


if __name__ == "__main__":
    main()
