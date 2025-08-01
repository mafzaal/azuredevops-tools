# MCP Server Integration - Git Tools

## Overview

The Azure DevOps Tools package has been successfully enhanced with comprehensive Git functionality and integrated into the Model Context Protocol (MCP) server. The server now provides **21 tools** across 5 categories for complete Azure DevOps automation.

## MCP Server Details

- **Server Name**: `devops_tools`
- **Version**: `0.2.0`
- **Description**: Comprehensive Azure DevOps Tools including Git repositories, pull requests, builds, changesets, and approval workflows
- **Transport**: stdio (compatible with LLMs)
- **Total Tools**: 21

## Tool Categories & Count

### 📄 Changeset Tools (4 tools)
- `get_changeset_tool` - Get detailed changeset information
- `get_changeset_changes_tool` - Get summary of file changes in changeset
- `get_changeset_list_tool` - Get multiple changesets with filtering
- `get_file_diff_tool` - Get file diff within a changeset

### 🔨 Build Tools (6 tools)
- `get_build_tool` - Get comprehensive build information
- `get_builds_tool` - Get multiple builds with filtering
- `get_build_logs_tool` - Get build logs with preview
- `get_build_log_full_content_tool` - Get complete build log content
- `get_failed_tasks_with_logs_tool` - Get failed tasks with recent logs
- `get_build_pipelines_tool` - Get all available pipelines

### 📦 Git Repository Tools (4 tools)
- `get_git_repositories_tool` - Get all Git repositories in project
- `get_git_repository_tool` - Get detailed repository information
- `get_git_commits_tool` - Get recent commits with details
- `get_git_commit_details_tool` - Get comprehensive commit information

### 🔀 Pull Request Tools (4 tools)
- `get_pull_requests_tool` - Get pull requests with filtering
- `get_pull_request_details_tool` - Get comprehensive PR information
- `create_pull_request_tool` - Create new pull request
- `get_pull_request_policies_tool` - Get branch policies and compliance

### ✅ Approval Workflow Tools (3 tools)
- `approve_pull_request_tool` - Approve a pull request (vote: 10)
- `reject_pull_request_tool` - Reject a pull request (vote: -10)
- `request_pull_request_changes_tool` - Request changes (vote: -5)

## Installation & Configuration

### Installation
```bash
# Install from source (development)
git clone <repository-url>
cd azuredevops-tools
uv pip install -e .

# Or install from PyPI (when published)
pip install azuredevops-tools
```

### Environment Configuration
Set up the required environment variables:

```bash
export DEVOPS_PAT="your-personal-access-token"
export DEVOPS_ORGANIZATION="your-organization"
export DEVOPS_PROJECT="your-project"
```

### MCP Configuration
Add to your MCP client configuration (e.g., `mcp-config.json`):

```json
{
  "mcpServers": {
    "azuredevops-tools": {
      "command": "uvx",
      "args": ["azuredevops-tools"],
      "env": {
        "DEVOPS_PAT": "your-personal-access-token",
        "DEVOPS_ORGANIZATION": "your-organization",
        "DEVOPS_PROJECT": "your-project"
      }
    }
  }
}
```

## Usage Examples

### Claude Desktop Configuration
For Claude Desktop, add to your configuration:

```json
{
  "mcpServers": {
    "azuredevops-tools": {
      "command": "uvx",
      "args": ["azuredevops-tools"],
      "env": {
        "DEVOPS_PAT": "your-pat-token",
        "DEVOPS_ORGANIZATION": "your-org",
        "DEVOPS_PROJECT": "your-project"
      }
    }
  }
}
```

### VS Code with MCP Extension
```json
{
  "servers": {
    "azuredevops-tools": {
      "type": "stdio",
      "command": "uvx",
      "args": ["azuredevops-tools"],
      "envFile": "${workspaceFolder}/.env"
    }
  }
}
```

## Key Features

### Git Repository Management
- **Repository Discovery**: Find and analyze all Git repositories
- **Commit Analysis**: Examine commit history and changes
- **Branch Information**: Get repository metadata and branch details

### Pull Request Workflows
- **PR Creation**: Programmatically create pull requests
- **Review Management**: Get PR details, reviewers, and status
- **Filtering**: Advanced filtering by status, branches, reviewers
- **Policy Compliance**: Check branch policies and requirements

### Approval Automation
- **Vote System**: Full Azure DevOps vote system support (-10 to +10)
- **Automated Approvals**: Programmatic PR approvals
- **Change Requests**: Request changes with feedback
- **Quality Gates**: Reject PRs that don't meet criteria

### Multi-Project Support
- **Project Targeting**: Optional project parameter on all tools
- **Default Fallback**: Uses environment configuration when project not specified
- **Consistent Interface**: Same parameter pattern across all tools

### Error Handling
- **Comprehensive Exception Handling**: All tools handle errors gracefully
- **Descriptive Messages**: Clear, actionable error descriptions
- **Logging Integration**: Full error logging for debugging
- **Graceful Degradation**: Partial data return when possible

## LLM Integration Features

### Optimized for AI
- **Descriptive Names**: Clear, intent-revealing function names
- **Rich Documentation**: Comprehensive docstrings with examples
- **Structured Output**: Human-readable, parseable responses
- **Consistent Interfaces**: Predictable patterns across tools

### Context-Aware
- **Parameter Flexibility**: Optional parameters with sensible defaults
- **Filtering Options**: Advanced filtering for precise results
- **Batch Operations**: Efficient handling of multiple requests
- **Status Information**: Rich metadata and status details

## Common Workflows

### Code Review Automation
```
1. get_pull_requests_tool("repo", "active") - Get active PRs
2. get_pull_request_details_tool("repo", pr_id) - Analyze PR
3. get_pull_request_policies_tool("repo", pr_id) - Check compliance
4. approve_pull_request_tool("repo", pr_id, reviewer) - Approve if criteria met
```

### Repository Audit
```
1. get_git_repositories_tool() - Discover all repositories
2. get_git_commits_tool(repo, "main", 10) - Check recent activity
3. get_pull_requests_tool(repo, "active") - Check open PRs
4. Generate audit report
```

### Release Management
```
1. get_git_commits_tool("repo", "main", 50) - Get commits since last release
2. get_git_commit_details_tool("repo", commit_id) - Analyze changes
3. create_pull_request_tool(...) - Create release PR
4. get_pull_request_policies_tool(...) - Verify release requirements
```

## Testing & Verification

### Server Verification
Run the test script to verify all tools are properly registered:

```bash
cd azuredevops-tools
uv run python tests/test_mcp_simple.py
```

Expected output:
```
✅ ALL TESTS PASSED!
✅ MCP Server is ready with 21 tools!
✅ The server can now be used with LLMs through the Model Context Protocol.
```

### Manual Testing
Test the server directly:

```bash
# Test server creation
uvx azuredevops-tools

# Test with timeout (expected)
timeout 5s uvx azuredevops-tools
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `uv pip install -e .`
   - Check Python version: Requires Python 3.11+

2. **Authentication Errors**
   - Verify DEVOPS_PAT is valid and has necessary permissions
   - Check DEVOPS_ORGANIZATION and DEVOPS_PROJECT are correct

3. **Permission Errors**
   - PAT needs permissions for: Code (read/write), Pull Request (read/write), Project and Team (read)

4. **Network Issues**
   - Verify connectivity to Azure DevOps
   - Check if behind corporate firewall

### Debug Mode
Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Planned Features
- **Advanced Filtering**: More sophisticated search capabilities
- **Bulk Operations**: Multi-PR operations
- **Webhook Integration**: Event-driven workflows
- **Analytics**: Metrics and reporting
- **Custom Policies**: User-defined approval workflows

### Performance Optimizations
- **Caching**: Reduce API call overhead
- **Batch Operations**: Combine multiple requests
- **Parallel Processing**: Concurrent operations
- **Smart Filtering**: Server-side optimization

## Conclusion

The MCP server integration provides a comprehensive, production-ready solution for Azure DevOps automation through LLMs. With 21 tools across 5 categories, it supports complete DevOps workflows from repository management to pull request approvals.

The server is optimized for LLM integration while maintaining flexibility for direct programmatic access. Comprehensive error handling, documentation, and testing ensure reliability and ease of use.

**The Azure DevOps Tools MCP server is ready for production use with LLMs!** 🚀
