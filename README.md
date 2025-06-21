# Azure DevOps Tools for LLM/MCP Integration

A comprehensive collection of Azure DevOps tools designed for seamless integration with Large Language Models (LLMs) through the Model Context Protocol (MCP). These tools enable AI assistants to interact with Azure DevOps for changeset analysis, build monitoring, pipeline management, and diagnostics.

## 🚀 Features

### Tool Categories

- **🔄 Changeset Tools**: Analyze code changes, file diffs, and modification history
- **🔨 Build Tools**: Monitor builds, analyze results, and retrieve logs  
- **⚙️ Pipeline Tools**: Manage CI/CD pipelines and definitions
- **🔧 Diagnostic Tools**: Debug failed builds and troubleshoot issues

### Available Tools

All tools support an optional `project` parameter to target specific Azure DevOps projects.

| Tool Name | Category | Description | Use Cases |
|-----------|----------|-------------|-----------|
| `get_changeset_tool` | changeset | Get detailed changeset information | Code review, audit trail |
| `get_file_diff_tool` | changeset | Get file diff within a changeset | Code review, debugging |
| `get_changeset_changes_tool` | changeset | Get summary of all file changes | Change overview, impact analysis |
| `get_changeset_list_tool` | changeset | Get multiple changesets with filtering | Recent changes, developer activity |
| `get_build_tool` | build | Get comprehensive build information | Build monitoring, status checking |
| `get_builds_tool` | build | Get multiple builds with filtering | Build history, trend analysis |
| `get_build_logs_tool` | build | Get build logs with preview | Quick log review, initial diagnosis |
| `get_build_log_full_content_tool` | build | Get complete build log content | Detailed analysis, thorough debugging |
| `get_failed_tasks_with_logs_tool` | diagnostic | Get failed tasks with recent logs | Build failure analysis, troubleshooting |
| `get_build_pipelines_tool` | pipeline | Get all available pipelines | Pipeline discovery, management |

## 📦 Installation

### Option 1: Install as Package (Recommended)

```bash
# Clone and install in development mode
git clone <repository-url>
cd azuredevops-tools
uv pip install -e .

# Or install from PyPI (when published)
pip install azuredevops-tools
```

### Option 2: Local Development

```bash
git clone <repository-url>
cd azuredevops-tools
uv sync
```

## 🔧 Configuration

Create a `.env` file in your project root with your Azure DevOps credentials:

```env
DEVOPS_PAT=your_personal_access_token
DEVOPS_ORGANIZATION=your_organization_name
DEVOPS_PROJECT=your_project_name
```

## 🔧 Usage

### As an Installed Package

```python
from azuredevops_tools import get_changeset_tool, get_build_tool

# Get changeset information (using default project)
changeset_info = get_changeset_tool(12345)
print(changeset_info)

# Get changeset from specific project
changeset_info = get_changeset_tool(12345, project="SpecificProject")
print(changeset_info)

# Get build information  
build_info = get_build_tool(67890)
print(build_info)

# Get build from specific project
build_info = get_build_tool(67890, project="AnotherProject")
print(build_info)
```

### Multi-Project Support

All tools support an optional `project` parameter to target specific Azure DevOps projects:

```python
# Using default project (from DEVOPS_PROJECT environment variable)
changesets = get_changeset_list_tool(author="John Doe")
builds = get_builds_tool(top=5)

# Using specific project
changesets = get_changeset_list_tool(author="John Doe", project="ProjectA")
builds = get_builds_tool(top=5, project="ProjectB")

# Comparing data across projects
project_a_builds = get_builds_tool(definition_id=139, project="ProjectA")
project_b_builds = get_builds_tool(definition_id=139, project="ProjectB")
```

**Benefits:**
- Work with multiple Azure DevOps projects using the same tool instance
- Compare data across different projects
- Maintain separate project contexts for different workflows
- Fallback to default project when project parameter is not specified

### Direct Tool Usage (Local Development)

```python
from src.azuredevops_tools.tools import get_changeset_tool, get_build_tool

# Get changeset information (using default project)
changeset_info = get_changeset_tool(12345)
print(changeset_info)

# Get changeset from specific project
changeset_info = get_changeset_tool(12345, project="MyProject")
print(changeset_info)

# Get build information  
build_info = get_build_tool(67890)
print(build_info)
```

### MCP Server

Start the MCP server to expose tools for LLM integration:

```bash
python mcp_server.py
```

The server provides a JSON-RPC interface over STDIO for MCP clients.

### Tool Discovery

```python
from tools import get_available_tools, get_tools_by_category

# Get all available tools
all_tools = get_available_tools()
print(f"Total tools: {all_tools['total_tools']}")

# Get tools by category
build_tools = get_tools_by_category("build")
print(f"Build tools: {build_tools['tool_count']}")
```

## 🤖 LLM Integration

### MCP Configuration

The `mcp-config.json` file provides tool schema for MCP clients:

```json
{
  "mcpVersion": "2024-11-05",
  "name": "azuredevops-tools",
  "description": "Azure DevOps Tools for LLM/MCP Integration",
  "tools": {
    "get_changeset_tool": {
      "description": "Get a specific changeset and summarize its details",
      "inputSchema": { ... }
    }
  }
}
```

### Tool Registry

Each tool includes comprehensive metadata for LLM discovery:

- **Clear descriptions**: Purpose and functionality
- **Parameter specifications**: Types and requirements  
- **Return value details**: What to expect
- **Use case examples**: When to use each tool
- **Category organization**: Logical grouping

## 📋 Tool Examples

### Changeset Analysis
```python
# Get recent changesets by author (default project)
changesets = get_changeset_list_tool(author="John Doe", from_changeset_id=12340)

# Get recent changesets by author (specific project)  
changesets = get_changeset_list_tool(author="John Doe", from_changeset_id=12340, project="MyProject")

# Analyze specific changeset changes
changes = get_changeset_changes_tool(12345)

# Get file diff for code review
diff = get_file_diff_tool("src/main.py", 12345)

# Get file diff from specific project
diff = get_file_diff_tool("src/main.py", 12345, project="SpecificProject")
```

### Build Monitoring
```python
# Check recent builds (default project)
builds = get_builds_tool(top=10, status_filter="completed")

# Check recent builds (specific project)
builds = get_builds_tool(top=10, status_filter="completed", project="MyProject")

# Get failed build details
failed_tasks = get_failed_tasks_with_logs_tool(67890)

# Get failed build details from specific project
failed_tasks = get_failed_tasks_with_logs_tool(67890, project="AnotherProject")

# Review build logs
logs = get_build_logs_tool(67890)
```

### Pipeline Management
```python
# Discover available pipelines (default project)
pipelines = get_build_pipelines_tool()

# Discover pipelines from specific project
pipelines = get_build_pipelines_tool(project="MyProject")

# Monitor specific pipeline builds
pipeline_builds = get_builds_tool(definition_id=139, top=5)

# Monitor pipeline builds from specific project
pipeline_builds = get_builds_tool(definition_id=139, top=5, project="TargetProject")
```

## 🔍 Tool Categories

### Changeset Tools
- **Purpose**: Analyze code modifications and version history
- **Key Features**: File diffs, change summaries, author filtering
- **Best For**: Code review, change impact analysis, audit trails

### Build Tools  
- **Purpose**: Monitor build execution and results
- **Key Features**: Status tracking, log analysis, timing information
- **Best For**: CI/CD monitoring, build failure investigation

### Pipeline Tools
- **Purpose**: Manage build definitions and configurations  
- **Key Features**: Pipeline discovery, metadata retrieval
- **Best For**: Pipeline administration, configuration management

### Diagnostic Tools
- **Purpose**: Troubleshoot build failures and issues
- **Key Features**: Failed task identification, log extraction
- **Best For**: Problem diagnosis, failure analysis, debugging

## 🛠️ Development

### Adding New Tools

1. Create the tool function in `tools.py`:
```python
def your_new_tool(param: int) -> str:
    """
    Clear description for LLMs.
    
    Parameters:
        param (int): Parameter description
        
    Returns:
        str: Return value description
    """
    # Implementation
    pass
```

2. Add to tool registry:
```python
TOOL_REGISTRY["your_new_tool"] = {
    "category": "appropriate_category",
    "description": "Clear tool description",
    "parameters": ["param: int"],
    "returns": "Return description",
    "use_cases": ["use case 1", "use case 2"]
}
```

3. Update MCP configuration and exports

### Testing

```bash
# Test individual tools
python -c "from tools import get_changeset_tool; print(get_changeset_tool(12345))"

# Test MCP server
echo '{"method": "tools/list"}' | python mcp_server.py
```

## 📝 Best Practices

### For LLM Integration

1. **Use descriptive tool names** that clearly indicate purpose
2. **Provide comprehensive docstrings** with examples
3. **Include error handling** with meaningful error messages
4. **Categorize tools logically** for easy discovery
5. **Document use cases** to help LLMs choose appropriate tools

### For MCP Compatibility

1. **Follow MCP schema standards** for tool definitions
2. **Use proper type annotations** for parameters
3. **Provide input validation** and error responses
4. **Include tool metadata** for discovery
5. **Test with actual MCP clients** before deployment

## 📚 References

- [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol)
- [Azure DevOps REST API](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tool documentation
4. Test with MCP clients
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details
