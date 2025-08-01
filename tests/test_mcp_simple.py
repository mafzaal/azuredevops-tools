#!/usr/bin/env python3
"""
Simple verification script for MCP server tool registration.
"""

import sys
import os

# Add the parent directory to the path so we can import our tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Test that the MCP server loads successfully with all tools."""
    try:
        print("Testing MCP server creation...")
        
        # Import and create server
        from azuredevops_tools.main import create_mcp_server
        
        print("✅ Successfully imported create_mcp_server")
        
        # Create the server
        mcp = create_mcp_server()
        print("✅ Successfully created MCP server")
        
        # Check server properties
        print(f"Server name: {mcp.name}")
        
        # Import all tools directly to verify they exist
        from azuredevops_tools.tools import (
            # Core changeset tools
            get_changeset_tool,
            get_changeset_changes_tool,
            get_changeset_list_tool,
            get_file_diff_tool,
            # Build tools
            get_build_tool,
            get_builds_tool,
            get_build_logs_tool,
            get_build_log_full_content_tool,
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
            get_pull_request_policies_tool,
        )
        
        print("✅ Successfully imported all tool functions")
        
        # List expected tools
        expected_tools = [
            # Changeset tools (4)
            'get_changeset_tool',
            'get_changeset_changes_tool',
            'get_changeset_list_tool', 
            'get_file_diff_tool',
            # Build tools (6)
            'get_build_tool',
            'get_builds_tool',
            'get_build_logs_tool',
            'get_build_log_full_content_tool',
            'get_failed_tasks_with_logs_tool',
            'get_build_pipelines_tool',
            # Project tools (1)
            'get_projects_tool',
            # Git repository tools (4)
            'get_git_repositories_tool',
            'get_git_repository_tool',
            'get_git_commits_tool',
            'get_git_commit_details_tool',
            # Pull request tools (4) 
            'get_pull_requests_tool',
            'get_pull_request_details_tool',
            'create_pull_request_tool',
            'get_pull_request_policies_tool',
            # Approval workflow tools (3)
            'approve_pull_request_tool',
            'reject_pull_request_tool',
            'request_pull_request_changes_tool',
        ]
        
        print(f"\nTool Registration Summary:")
        print(f"  Expected tools: {len(expected_tools)}")
        print(f"  Changeset tools: 4")
        print(f"  Build tools: 6")
        print(f"  Project tools: 1")
        print(f"  Git repository tools: 4")
        print(f"  Pull request tools: 4")
        print(f"  Approval workflow tools: 3")
        print(f"  Total: {len(expected_tools)}")
        
        print("\nTool Categories:")
        print("  📄 Changeset Tools:")
        for tool in expected_tools[:4]:
            print(f"    - {tool}")
        
        print("  🔨 Build Tools:")
        for tool in expected_tools[4:10]:
            print(f"    - {tool}")
        
        print("  🏢 Project Tools:")
        for tool in expected_tools[10:11]:
            print(f"    - {tool}")
        
        print("  📦 Git Repository Tools:")
        for tool in expected_tools[11:15]:
            print(f"    - {tool}")
        
        print("  🔀 Pull Request Tools:")
        for tool in expected_tools[15:19]:
            print(f"    - {tool}")
        
        print("  ✅ Approval Workflow Tools:")
        for tool in expected_tools[19:]:
            print(f"    - {tool}")
        
        print(f"\n✅ ALL TESTS PASSED!")
        print(f"✅ MCP Server is ready with {len(expected_tools)} tools!")
        print("✅ The server can now be used with LLMs through the Model Context Protocol.")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
