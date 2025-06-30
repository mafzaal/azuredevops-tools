#!/usr/bin/env python3
"""
Test script to verify that all Azure DevOps tools are properly registered with the MCP server.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_mcp_server():
    """Test the MCP server creation and tool registration."""
    try:
        # Import the MCP server creation function
        from azuredevops_tools.main import create_mcp_server
        
        # Create the server
        server = create_mcp_server()
        
        print("✅ MCP Server created successfully!")
        print(f"📋 Server name: {server.name}")
        
        # Get registered tools from server's handlers
        registered_tools = []
        if hasattr(server, '_handlers') and hasattr(server._handlers, 'tools'):
            registered_tools = list(server._handlers.tools.keys())
        elif hasattr(server, 'tools'):
            registered_tools = list(server.tools.keys())
        
        print(f"🛠️  Number of tools registered: {len(registered_tools)}")
        
        if registered_tools:
            print("\n📚 Registered tools:")
            for i, tool_name in enumerate(sorted(registered_tools), 1):
                print(f"  {i:2d}. {tool_name}")
        else:
            print("\n⚠️  Could not access registered tools list")
        
        # Test that all expected tools are registered
        expected_tools = [
            # Changeset tools
            "get_changeset_tool",
            "get_file_diff_tool", 
            "get_changeset_changes_tool",
            "get_changeset_list_tool",
            
            # Build tools
            "get_build_tool",
            "get_builds_tool",
            "get_build_logs_tool",
            "get_build_log_full_content_tool",
            "get_failed_tasks_with_logs_tool",
            "get_build_pipelines_tool",
            
            # Git repository tools
            "get_git_repositories_tool",
            "get_git_repository_tool",
            "get_git_commits_tool",
            "get_git_commit_details_tool",
            
            # Pull request tools
            "get_pull_requests_tool",
            "get_pull_request_details_tool",
            "create_pull_request_tool",
            "approve_pull_request_tool",
            "reject_pull_request_tool",
            "request_pull_request_changes_tool",
            "get_pull_request_policies_tool",
        ]
        
        print(f"\n🔍 Checking for expected tools ({len(expected_tools)} expected):")
        missing_tools = []
        for tool in expected_tools:
            if tool in registered_tools:
                print(f"  ✅ {tool}")
            else:
                print(f"  ❌ {tool} (MISSING)")
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"\n⚠️  WARNING: {len(missing_tools)} tools are missing from the MCP server!")
            return False
        else:
            print(f"\n🎉 SUCCESS: All {len(expected_tools)} expected tools are registered!")
            return True
            
    except Exception as e:
        print(f"❌ Error creating MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tool_imports():
    """Test that all tools can be imported directly."""
    try:
        from azuredevops_tools.tools import __all__
        print(f"\n📦 Testing tool imports ({len(__all__)} tools in __all__):")
        
        # Import all tools dynamically
        from azuredevops_tools import tools
        imported_tools = []
        
        for tool_name in __all__:
            if hasattr(tools, tool_name):
                tool_func = getattr(tools, tool_name)
                if callable(tool_func):
                    print(f"  ✅ {tool_name}")
                    imported_tools.append(tool_name)
                else:
                    print(f"  ❌ {tool_name} (not callable)")
            else:
                print(f"  ❌ {tool_name} (not found in module)")
        
        print(f"\n📊 Import summary: {len(imported_tools)}/{len(__all__)} tools imported successfully")
        return len(imported_tools) == len(__all__)
        
    except Exception as e:
        print(f"❌ Error testing tool imports: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Azure DevOps MCP Tools Registration\n")
    print("=" * 60)
    
    # Test tool imports
    import_success = test_tool_imports()
    
    print("\n" + "=" * 60)
    
    # Test MCP server
    server_success = test_mcp_server()
    
    print("\n" + "=" * 60)
    
    if import_success and server_success:
        print("🎉 ALL TESTS PASSED! The MCP server is ready to use.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED! Please check the issues above.")
        sys.exit(1)
