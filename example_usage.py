#!/usr/bin/env python3
"""
Example Usage of Azure DevOps Tools

This script demonstrates how to use the Azure DevOps tools for
various scenarios like changeset analysis, build monitoring,
and pipeline management.
"""

from tools import (
    get_changeset_tool,
    get_file_diff_tool,
    get_changeset_changes_tool,
    get_changeset_list_tool,
    get_build_tool,
    get_builds_tool,
    get_build_logs_tool,
    get_failed_tasks_with_logs_tool,
    get_build_pipelines_tool,
    get_available_tools,
    get_tools_by_category
)

def demo_changeset_analysis():
    """Demonstrate changeset analysis tools"""
    print("=== Changeset Analysis Demo ===\n")
    
    # Get recent changesets
    print("1. Getting recent changesets...")
    changesets = get_changeset_list_tool(from_changeset_id=12340, to_changeset_id=12350)
    print(changesets)
    print()
    
    # Analyze specific changeset
    print("2. Analyzing specific changeset...")
    changeset_info = get_changeset_tool(12345)
    print(changeset_info)
    print()
    
    # Get file changes in changeset
    print("3. Getting file changes...")
    changes = get_changeset_changes_tool(12345)
    print(changes)
    print()
    
    # Get specific file diff
    print("4. Getting file diff...")
    diff = get_file_diff_tool("src/main.py", 12345)
    print(diff)
    print()

def demo_build_monitoring():
    """Demonstrate build monitoring tools"""
    print("=== Build Monitoring Demo ===\n")
    
    # Get recent builds
    print("1. Getting recent builds...")
    builds = get_builds_tool(top=5, status_filter="completed")
    print(builds)
    print()
    
    # Get specific build info
    print("2. Getting specific build information...")
    build_info = get_build_tool(67890)
    print(build_info)
    print()
    
    # Get build logs preview
    print("3. Getting build logs preview...")
    logs = get_build_logs_tool(67890)
    print(f"Build {logs.get('buildId')} has {logs.get('totalLogs')} logs")
    for log in logs.get('logs', []):
        print(f"  - Log {log['id']}: {log['type']} ({log['contentLineCount']} lines)")
    print()
    
    # Analyze failed builds
    print("4. Analyzing failed tasks...")
    failed_tasks = get_failed_tasks_with_logs_tool(67891)  # Assuming this build failed
    print(failed_tasks[:500] + "..." if len(failed_tasks) > 500 else failed_tasks)
    print()

def demo_pipeline_management():
    """Demonstrate pipeline management tools"""
    print("=== Pipeline Management Demo ===\n")
    
    # Discover available pipelines
    print("1. Discovering available pipelines...")
    pipelines = get_build_pipelines_tool()
    print(pipelines[:500] + "..." if len(pipelines) > 500 else pipelines)
    print()
    
    # Get builds for specific pipeline
    print("2. Getting builds for specific pipeline...")
    pipeline_builds = get_builds_tool(definition_id=139, top=3)
    print(pipeline_builds)
    print()

def demo_tool_discovery():
    """Demonstrate tool discovery capabilities"""
    print("=== Tool Discovery Demo ===\n")
    
    # Get all available tools
    print("1. Getting all available tools...")
    all_tools = get_available_tools()
    print(f"Total tools: {all_tools['total_tools']}")
    print(f"Categories: {list(all_tools['tool_categories'].keys())}")
    print()
    
    # Get tools by category
    print("2. Getting tools by category...")
    categories = ["changeset", "build", "pipeline", "diagnostic"]
    
    for category in categories:
        category_tools = get_tools_by_category(category)
        print(f"\\n{category.upper()} TOOLS ({category_tools['tool_count']} tools):")
        print(f"Description: {category_tools['description']}")
        for tool_name, tool_info in category_tools['tools'].items():
            print(f"  - {tool_name}: {tool_info['description']}")
    print()

def demo_error_handling():
    """Demonstrate error handling in tools"""
    print("=== Error Handling Demo ===\n")
    
    # Try to get non-existent changeset
    print("1. Testing with invalid changeset ID...")
    result = get_changeset_tool(999999)
    print(result)
    print()
    
    # Try to get non-existent build
    print("2. Testing with invalid build ID...")
    result = get_build_tool(999999)
    print(result)
    print()

def main():
    """Main demonstration function"""
    print("Azure DevOps Tools - Usage Examples")
    print("=" * 50)
    print()
    
    try:
        # Tool discovery first
        demo_tool_discovery()
        
        # Then demonstrate actual tool usage
        # Note: These will fail without proper Azure DevOps connection
        # but show the expected usage patterns
        
        print("\\nNote: The following demos require Azure DevOps connection.")
        print("They are shown for demonstration purposes:\\n")
        
        demo_changeset_analysis()
        demo_build_monitoring() 
        demo_pipeline_management()
        demo_error_handling()
        
    except Exception as e:
        print(f"Demo error (expected without Azure DevOps connection): {e}")
        print("\\nThis is normal - the tools require Azure DevOps authentication.")
        print("See README.md for setup instructions.")
    
    print("\\n=== Demo Complete ===")
    print("\\nFor actual usage:")
    print("1. Configure Azure DevOps connection in devops_tools.py")
    print("2. Use tools individually or through MCP server")
    print("3. Integrate with LLMs using the MCP protocol")

if __name__ == "__main__":
    main()
