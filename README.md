# Azure DevOps Tools for LLM/MCP Integration

A comprehensive collection of Azure DevOps tools designed for seamless integration with Large Language Models (LLMs) through the Model Context Protocol (MCP). These tools enable AI assistants to interact with Azure DevOps for changeset analysis, build monitoring, pipeline management, and diagnostics.

## 🚀 Features

### Tool Categories

- **🔄 Changeset Tools**: Analyze code changes, file diffs, and modification history
- **🔨 Build Tools**: Monitor builds, analyze results, and retrieve logs  
- **⚙️ Pipeline Tools**: Manage CI/CD pipelines and definitions
- **🔧 Diagnostic Tools**: Debug failed builds and troubleshoot issues
- **📦 Git Repository Tools**: Discover and manage Git repositories
- **🔀 Pull Request Tools**: Create, review, and manage pull requests
- **✅ Approval Workflow Tools**: Handle code review and approval processes

### Available Tools

All tools support an optional `project` parameter to target specific Azure DevOps projects.

#### Core Azure DevOps Tools

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
| `get_projects_tool` | project | Get all projects in the organization | Project discovery, management |

#### Git Repository Tools

| Tool Name | Category | Description | Use Cases |
|-----------|----------|-------------|-----------|
| `get_git_repositories_tool` | git | Get all Git repositories in project | Repository discovery, inventory |
| `get_git_repository_tool` | git | Get detailed repository information | Repository analysis, metadata |
| `get_git_commits_tool` | git | Get recent commits with details | Commit history, developer activity |
| `get_git_commit_details_tool` | git | Get comprehensive commit information | Code review, change analysis |

#### Pull Request Tools

| Tool Name | Category | Description | Use Cases |
|-----------|----------|-------------|-----------|
| `get_pull_requests_tool` | pull-request | Get pull requests with filtering | PR monitoring, review queue |
| `get_pull_request_details_tool` | pull-request | Get comprehensive PR information | Code review, approval status |
| `create_pull_request_tool` | pull-request | Create new pull request | Automated PR creation, workflows |
| `get_pull_request_policies_tool` | pull-request | Get branch policies and compliance | Policy compliance, requirements |

#### Approval Workflow Tools

| Tool Name | Category | Description | Use Cases |
|-----------|----------|-------------|-----------|
| `approve_pull_request_tool` | approval | Approve a pull request | Automated approvals, workflows |
| `reject_pull_request_tool` | approval | Reject a pull request | Quality gates, review process |
| `request_pull_request_changes_tool` | approval | Request changes on PR | Code review, feedback process |

## 📦 Installation

### Option 1: Install from PyPI (Recommended)

```bash
# Install from PyPI
pip install azuredevops-tools

# Or using uv
uv add azuredevops-tools
```

### Option 2: Install from Source (Development)

```bash
# Clone and install in development mode
git clone <repository-url>
cd azuredevops-tools
uv pip install -e .
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

## 🤖 LLM Integration

### MCP Configuration

The `mcp.json` file provides configuration with clients:

```json
{
    "servers": {
        "azuredevops-tools": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "--directory",
                "${workspaceFolder}",
                "azuredevops-tools"
                
            ],
            "envFile": "${workspaceFolder}/.env",
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

### Git Repository and Pull Request Tools

The Git tools provide comprehensive support for Git repositories, commits, and pull request workflows:

#### Repository Discovery and Analysis

```python
from azuredevops_tools.tools import (
    get_git_repositories_tool,
    get_git_repository_tool,
    get_git_commits_tool,
    get_git_commit_details_tool
)

# Discover all Git repositories in the project
repositories = get_git_repositories_tool()
print(repositories)

# Get detailed information about a specific repository
repo_details = get_git_repository_tool("my-app")
print(repo_details)

# Get recent commits from main branch
commits = get_git_commits_tool("my-app", "main", top=10)
print(commits)

# Get detailed information about a specific commit
commit_details = get_git_commit_details_tool("my-app", "abc123def456")
print(commit_details)
```

#### Pull Request Management

```python
from azuredevops_tools.tools import (
    get_pull_requests_tool,
    get_pull_request_details_tool,
    create_pull_request_tool,
    get_pull_request_policies_tool
)

# Get active pull requests
active_prs = get_pull_requests_tool("my-app", status="active")
print(active_prs)

# Get pull requests targeting main branch
main_prs = get_pull_requests_tool("my-app", target_branch="main")
print(main_prs)

# Get detailed information about a specific PR
pr_details = get_pull_request_details_tool("my-app", 123)
print(pr_details)

# Create a new pull request
new_pr = create_pull_request_tool(
    repository_id="my-app",
    title="Fix authentication bug",
    description="This PR fixes the authentication issue...",
    source_branch="feature/auth-fix",
    target_branch="main",
    reviewers=["reviewer1@company.com", "reviewer2@company.com"]
)
print(new_pr)

# Check branch policies for a PR
policies = get_pull_request_policies_tool("my-app", 123)
print(policies)
```

#### Code Review and Approval Workflows

```python
from azuredevops_tools.tools import (
    approve_pull_request_tool,
    reject_pull_request_tool,
    request_pull_request_changes_tool
)

# Approve a pull request
approval = approve_pull_request_tool("my-app", 123, "reviewer@company.com")
print(approval)

# Request changes on a pull request
changes = request_pull_request_changes_tool("my-app", 123, "reviewer@company.com")
print(changes)

# Reject a pull request
rejection = reject_pull_request_tool("my-app", 123, "reviewer@company.com")
print(rejection)
```

#### Complete Workflow Example

```python
# 1. Repository Analysis
repos = get_git_repositories_tool()
print(f"Found {len(repos)} repositories")

# 2. Commit History Analysis
for repo in repos:
    commits = get_git_commits_tool(repo['name'], top=5)
    print(f"Recent commits in {repo['name']}: {len(commits)}")

# 3. Pull Request Review
active_prs = get_pull_requests_tool("my-app", "active")
for pr in active_prs:
    pr_details = get_pull_request_details_tool("my-app", pr['pullRequestId'])
    policies = get_pull_request_policies_tool("my-app", pr['pullRequestId'])
    
    print(f"PR #{pr['pullRequestId']}: {pr['title']}")
    print(f"Reviewers: {len(pr_details['reviewers'])}")
    print(f"Policies: {len(policies)}")

# 4. Automated Approval (if conditions met)
if all_conditions_met:
    approval = approve_pull_request_tool("my-app", pr_id, "auto-reviewer@company.com")
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

### Project Structure

```
azuredevops-tools/
├── .github/workflows/          # CI/CD workflows
│   ├── ci.yml                 # Continuous Integration
│   └── publish.yml            # PyPI Publishing
├── src/azuredevops_tools/     # Main package source
├── tests/                     # Test suite
├── examples/                  # Usage examples
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

### Local Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd azuredevops-tools

# Install with development dependencies
uv sync --all-extras

# Or use the Makefile
make install
```

#### Development Commands

```bash
# Run tests
make test
# or with coverage
make test-cov

# Check code quality
make lint

# Format code
make format

# Build package
make build

# Clean build artifacts
make clean

# Publish to Test PyPI
make publish-test

# Publish to PyPI
make publish
```

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

#### Continuous Integration (`ci.yml`)
- **Triggers**: Push to `main`/`develop` branches, pull requests
- **Matrix Testing**: Python 3.11, 3.12, 3.13
- **Steps**: 
  - Install dependencies with uv
  - Run tests with pytest
  - Run code quality checks (black, isort, flake8)
  - Upload coverage reports
  - Build and validate package

#### Publishing Workflow (`publish.yml`)
- **Triggers**: 
  - GitHub releases (automatic PyPI publish)
  - Manual workflow dispatch (with Test PyPI option)
- **Security**: Uses trusted publishing (OIDC) - no API tokens needed
- **Steps**:
  - Run full test suite across Python versions
  - Build wheel and source distributions
  - Validate package with twine
  - Publish to PyPI or Test PyPI

### Publishing to PyPI

#### Automatic Publishing (Recommended)
1. **Set up trusted publishing**:
   - Go to PyPI → Account settings → Publishing
   - Add GitHub repository as trusted publisher
   - Environment name: `pypi` (for production) or `testpypi` (for testing)

2. **Create a release**:
   ```bash
   # Update version in pyproject.toml and __init__.py
   git tag v0.1.1
   git push origin v0.1.1
   ```
   
3. **Create GitHub release**: The workflow will automatically publish to PyPI

#### Manual Publishing
```bash
# Build the package
uv build

# Publish to Test PyPI (optional)
uv run twine upload --repository testpypi dist/*

# Publish to PyPI
uv run twine upload dist/*
```

#### Testing Published Package
```bash
# Test from Test PyPI (when published)
pip install --index-url https://test.pypi.org/simple/ azuredevops-tools

# Test from PyPI
pip install azuredevops-tools
```

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

2. Update MCP configuration and exports

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
