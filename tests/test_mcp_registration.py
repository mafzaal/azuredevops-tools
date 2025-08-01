#!/usr/bin/env python3
"""
Test script to verify MCP server tool registration.

This script validates that all tools are properly registered with the MCP server
and can be discovered by LLMs.
"""

import sys
import os

# Add the parent directory to the path so we can import our tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from azuredevops_tools.main import create_mcp_server


def test_mcp_server_tools():
    """Test that all tools are properly registered with the MCP server."""
    print("Creating MCP server...")
    mcp = create_mcp_server()
    
    print(f"Server Name: {mcp.name}")
    print(f"Server Description: {mcp.description}")
    print(f"Server Version: {mcp.version}")
    print()
    
    # Get the list of registered tools
    import inspect
    import asyncio
    tools_coro = mcp.list_tools()
    if inspect.iscoroutine(tools_coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        tools = loop.run_until_complete(tools_coro)
    else:
        tools = tools_coro
    print(f"Total tools registered: {len(tools)}")
    print()
    
    # Categorize tools for better display
    tool_categories = {
        'Changeset Tools': [],
        'Build Tools': [],
        'Git Repository Tools': [],
        'Pull Request Tools': [],
        'Approval Workflow Tools': [],
        'Policy Tools': []
    }
    
    for tool in tools:
        tool_name = tool.name
        if 'changeset' in tool_name or 'file_diff' in tool_name:
            tool_categories['Changeset Tools'].append(tool_name)
        elif 'build' in tool_name:
            tool_categories['Build Tools'].append(tool_name)
        elif 'git_repositories' in tool_name or 'git_repository' in tool_name or 'git_commit' in tool_name:
            tool_categories['Git Repository Tools'].append(tool_name)
        elif 'pull_request' in tool_name and not any(x in tool_name for x in ['approve', 'reject', 'request', 'policies']):
            tool_categories['Pull Request Tools'].append(tool_name)
        elif any(x in tool_name for x in ['approve', 'reject', 'request']):
            tool_categories['Approval Workflow Tools'].append(tool_name)
        elif 'policies' in tool_name:
            tool_categories['Policy Tools'].append(tool_name)
    
    # Display tools by category
    for category, tools_list in tool_categories.items():
        if tools_list:
            print(f"{category}:")
            for tool_name in sorted(tools_list):
                # Find the tool object to get description
                tool_obj = next((t for t in tools if t.name == tool_name), None)
                if tool_obj and tool_obj.description:
                    description = tool_obj.description[:80] + "..." if len(tool_obj.description) > 80 else tool_obj.description
                    print(f"  - {tool_name}: {description}")
                elif tool_obj:
                    print(f"  - {tool_name}: No description provided.")
            print()
    
    # Verify expected tool counts
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
    
    registered_tool_names = [tool.name for tool in tools]
    
    print("Tool Registration Verification:")
    print(f"Expected tools: {len(expected_tools)}")
    print(f"Registered tools: {len(registered_tool_names)}")
    
    missing_tools = [tool for tool in expected_tools if tool not in registered_tool_names]
    unexpected_tools = [tool for tool in registered_tool_names if tool not in expected_tools]
    
    if missing_tools:
        print(f"❌ Missing tools: {missing_tools}")
    
    if unexpected_tools:
        print(f"⚠️  Unexpected tools: {unexpected_tools}")
    
    if not missing_tools and not unexpected_tools:
        print("✅ All tools registered successfully!")
    
    print()
    print("Tool Registration Summary:")
    print(f"  Changeset Tools: {len(tool_categories['Changeset Tools'])}")
    print(f"  Build Tools: {len(tool_categories['Build Tools'])}")
    print(f"  Git Repository Tools: {len(tool_categories['Git Repository Tools'])}")
    print(f"  Pull Request Tools: {len(tool_categories['Pull Request Tools'])}")
    print(f"  Approval Workflow Tools: {len(tool_categories['Approval Workflow Tools'])}")
    print(f"  Policy Tools: {len(tool_categories['Policy Tools'])}")
    print(f"  Total: {len(tools)}")
    
    return len(missing_tools) == 0 and len(unexpected_tools) == 0


def test_tool_parameters():
    """Test that tools have proper parameter definitions."""
    print("\nTesting tool parameter definitions...")
    mcp = create_mcp_server()
    import inspect
    tools_coro = mcp.list_tools()
    if inspect.iscoroutine(tools_coro):
        import asyncio
        tools = asyncio.get_event_loop().run_until_complete(tools_coro)
    else:
        tools = tools_coro

    issues = []

    for tool in tools:
        tool_name = tool.name
        # Check that all tools have descriptions
        if not getattr(tool, 'description', None):
            issues.append(f"{tool_name}: Missing description")
        # Check that tools have proper parameter definitions
        input_schema = getattr(tool, 'input_schema', None)
        if input_schema:
            properties = input_schema.get('properties', {})
            # All tools should have optional 'project' parameter
            if 'project' not in properties:
                issues.append(f"{tool_name}: Missing 'project' parameter")
            # Check required parameters exist
            required = input_schema.get('required', [])
            if tool_name in ['get_changeset_tool', 'get_build_tool'] and len(required) == 0:
                issues.append(f"{tool_name}: Should have required parameters")

    if issues:
        print("❌ Parameter definition issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ All tools have proper parameter definitions!")
    return len(issues) == 0


def main():
    """Main test function."""
    print("=" * 80)
    print("Azure DevOps Tools - MCP Server Registration Test")
    print("=" * 80)
    
    try:
        # Test tool registration
        tools_ok = test_mcp_server_tools()
        
        # Test parameter definitions
        params_ok = test_tool_parameters()
        
        print("\n" + "=" * 80)
        if tools_ok and params_ok:
            print("✅ ALL TESTS PASSED - MCP Server is ready!")
            print("The server can now be used with LLMs through the Model Context Protocol.")
        else:
            print("❌ SOME TESTS FAILED - Please review the issues above.")
        print("=" * 80)
        
        return 0 if (tools_ok and params_ok) else 1
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
