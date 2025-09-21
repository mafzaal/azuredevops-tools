# Azure DevOps Tools for LLM/MCP Integration

A comprehensive collection of Azure DevOps tools designed for seamless integration with Large Language Models (LLMs) through the Model Context Protocol (MCP). These tools enable AI assistants to interact with Azure DevOps for changeset analysis, build monitoring, pipeline management, Git repository operations, pull request workflows, and automated code review processes.

## 🚀 Quick Install in VS Code

### Install with uvx (Python Package)

[![Install in VS Code](https://img.shields.io/badge/Install%20in-VS%20Code-blue?style=for-the-badge&logo=visual-studio-code)](https://vscode.dev/redirect/mcp/install?name=azure-devops-mcp-server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22azuredevops-tools%22%5D%2C%22env%22%3A%7B%22DEVOPS_ORGANIZATION%22%3A%22%24%7Binput%3ADEVOPS_ORGANIZATION%7D%22%2C%22DEVOPS_PROJECT%22%3A%22%24%7Binput%3ADEVOPS_PROJECT%7D%22%2C%22DEVOPS_PAT%22%3A%22%24%7Binput%3ADEVOPS_PAT%7D%22%7D%7D&inputs=%5B%7B%22id%22%3A%22DEVOPS_ORGANIZATION%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20organization%20name%22%7D%2C%7B%22id%22%3A%22DEVOPS_PROJECT%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20project%20name%22%7D%2C%7B%22id%22%3A%22DEVOPS_PAT%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%20(PAT)%22%2C%22password%22%3Atrue%7D%5D)

[![Install in VS Code Insiders](https://img.shields.io/badge/Install%20in-VS%20Code%20Insiders-purple?style=for-the-badge&logo=visual-studio-code)](https://insiders.vscode.dev/redirect/mcp/install?name=azure-devops-mcp-server&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22azuredevops-tools%22%5D%2C%22env%22%3A%7B%22DEVOPS_ORGANIZATION%22%3A%22%24%7Binput%3ADEVOPS_ORGANIZATION%7D%22%2C%22DEVOPS_PROJECT%22%3A%22%24%7Binput%3ADEVOPS_PROJECT%7D%22%2C%22DEVOPS_PAT%22%3A%22%24%7Binput%3ADEVOPS_PAT%7D%22%7D%7D&inputs=%5B%7B%22id%22%3A%22DEVOPS_ORGANIZATION%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20organization%20name%22%7D%2C%7B%22id%22%3A%22DEVOPS_PROJECT%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20project%20name%22%7D%2C%7B%22id%22%3A%22DEVOPS_PAT%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%20(PAT)%22%2C%22password%22%3Atrue%7D%5D)

### Install with Docker

[![Install in VS Code (Docker)](https://img.shields.io/badge/Install%20in-VS%20Code%20(Docker)-blue?style=for-the-badge&logo=docker)](https://vscode.dev/redirect/mcp/install?name=azure-devops-mcp-server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22--rm%22%2C%22-i%22%2C%22-e%22%2C%22DEVOPS_ORGANIZATION%3D%24%7Binput%3ADEVOPS_ORGANIZATION%7D%22%2C%22-e%22%2C%22DEVOPS_PROJECT%3D%24%7Binput%3ADEVOPS_PROJECT%7D%22%2C%22-e%22%2C%22DEVOPS_PAT%3D%24%7Binput%3ADEVOPS_PAT%7D%22%2C%22ghcr.io%2Fmafzaal%2Fazuredevops-tools%3Alatest%22%5D%7D&inputs=%5B%7B%22id%22%3A%22DEVOPS_ORGANIZATION%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20organization%20name%22%7D%2C%7B%22id%22%3A%22DEVOPS_PROJECT%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20project%20name%22%7D%2C%7B%22id%22%3A%22DEVOPS_PAT%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%20(PAT)%22%2C%22password%22%3Atrue%7D%5D)

[![Install in VS Code Insiders (Docker)](https://img.shields.io/badge/Install%20in-VS%20Code%20Insiders%20(Docker)-purple?style=for-the-badge&logo=docker)](https://insiders.vscode.dev/redirect/mcp/install?name=azure-devops-mcp-server&quality=insiders&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22--rm%22%2C%22-i%22%2C%22-e%22%2C%22DEVOPS_ORGANIZATION%3D%24%7Binput%3ADEVOPS_ORGANIZATION%7D%22%2C%22-e%22%2C%22DEVOPS_PROJECT%3D%24%7Binput%3ADEVOPS_PROJECT%7D%22%2C%22-e%22%2C%22DEVOPS_PAT%3D%24%7Binput%3ADEVOPS_PAT%7D%22%2C%22ghcr.io%2Fmafzaal%2Fazuredevops-tools%3Alatest%22%5D%7D&inputs=%5B%7B%22id%22%3A%22DEVOPS_ORGANIZATION%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20organization%20name%22%7D%2C%7B%22id%22%3A%22DEVOPS_PROJECT%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20project%20name%22%7D%2C%7B%22id%22%3A%22DEVOPS_PAT%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Azure%20DevOps%20Personal%20Access%20Token%20(PAT)%22%2C%22password%22%3Atrue%7D%5D)

## 🚀 Features

### Tool Categories

- **🔄 Changeset Tools**: Analyze TFVC code changes, file diffs, and modification history
- **🔨 Build Tools**: Monitor builds, analyze results, and retrieve comprehensive logs  
- **⚙️ Pipeline Tools**: Discover and manage CI/CD pipelines and definitions
- **🔧 Diagnostic Tools**: Debug failed builds and troubleshoot issues with detailed logs
- **📦 Git Repository Tools**: Discover, analyze, and manage Git repositories and commits
- **🔀 Pull Request Tools**: Create, review, and manage pull requests with full workflow support
- **✅ Approval Workflow Tools**: Handle automated code review and approval processes
- **🏢 Project Management Tools**: Discover and manage projects across the Azure DevOps organization

### Key Capabilities

- **22 Comprehensive Tools** covering all major Azure DevOps operations
- **Multi-Project Support** with optional project parameter on all tools
- **Detailed Error Handling** with meaningful error messages for LLM interpretation
- **Rich Output Formatting** optimized for LLM consumption and analysis
- **Cross-Platform Compatibility** supporting both TFVC and Git repositories
- **Automated Workflows** enabling complex DevOps automation scenarios
- **MCP-Optimized** with comprehensive tool metadata for optimal LLM discovery

### Available Tools

All tools support an optional `project` parameter to target specific Azure DevOps projects.

#### Core Azure DevOps Tools

| Tool Name | Category | Description | Use Cases |
|-----------|----------|-------------|-----------|
| `get_changeset_tool` | changeset | Get detailed changeset information with ID, comment, author, and date | Code review, audit trail |
| `get_file_diff_tool` | changeset | Get line-by-line file diff within a changeset | Code review, debugging |
| `get_changeset_changes_tool` | changeset | Get summary of all file changes (excludes binary files) | Change overview, impact analysis |
| `get_changeset_list_tool` | changeset | Get multiple changesets with author and ID range filtering | Recent changes, developer activity |
| `get_build_tool` | build | Get comprehensive build information including status, result, duration | Build monitoring, status checking |
| `get_builds_tool` | build | Get multiple builds with definition, status, and count filtering | Build history, trend analysis |
| `get_build_logs_tool` | build | Get build logs with preview content (first 50 lines) | Quick log review, initial diagnosis |
| `get_build_log_full_content_tool` | build | Get complete untruncated build log content with metadata | Detailed analysis, thorough debugging |
| `get_failed_tasks_with_logs_tool` | diagnostic | Get failed tasks with last 200 lines of logs for troubleshooting | Build failure analysis, troubleshooting |
| `get_build_pipelines_tool` | pipeline | Get all available build pipelines with IDs, names, and metadata | Pipeline discovery, management |
| `get_projects_tool` | project | Get all projects in the organization with descriptions and metadata | Project discovery, management |

#### Git Repository Tools

| Tool Name | Category | Description | Use Cases |
|-----------|----------|-------------|-----------|
| `get_git_repositories_tool` | git | Get all Git repositories with URLs, branches, and metadata | Repository discovery, inventory |
| `get_git_repository_tool` | git | Get detailed repository information including size and status | Repository analysis, metadata |
| `get_git_commits_tool` | git | Get recent commits with messages, authors, and change statistics | Commit history, developer activity |
| `get_git_commit_details_tool` | git | Get comprehensive commit info with full message and file changes | Code review, change analysis |

#### Pull Request Tools

| Tool Name | Category | Description | Use Cases |
|-----------|----------|-------------|-----------|
| `get_pull_requests_tool` | pull-request | Get PRs with status, branch, and reviewer filtering | PR monitoring, review queue |
| `get_pull_request_details_tool` | pull-request | Get comprehensive PR info with reviewers and linked work items | Code review, approval status |
| `create_pull_request_tool` | pull-request | Create new PR with title, description, reviewers, and draft option | Automated PR creation, workflows |
| `get_pull_request_policies_tool` | pull-request | Get branch policies and their evaluation status for compliance | Policy compliance, requirements |

#### Approval Workflow Tools

| Tool Name | Category | Description | Use Cases |
|-----------|----------|-------------|-----------|
| `approve_pull_request_tool` | approval | Approve a PR by casting vote of 10 (Approved) | Automated approvals, workflows |
| `reject_pull_request_tool` | approval | Reject a PR by casting vote of -10 (Rejected) | Quality gates, review process |
| `request_pull_request_changes_tool` | approval | Request changes by casting vote of -5 (Waiting for Author) | Code review, feedback process |

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

# Discover all Git repositories in the default project
repositories = get_git_repositories_tool()
print(repositories)
# Output: Repository details with IDs, URLs, default branches, sizes

# Discover repositories in a specific project
repositories = get_git_repositories_tool(project="MyProject")
print(repositories)

# Get detailed information about a specific repository
repo_details = get_git_repository_tool("my-app")
print(repo_details)
# Output: Name, ID, default branch, size, URLs, status

# Get recent commits from main branch (default: 10 commits)
commits = get_git_commits_tool("my-app", "main", top=10)
print(commits)
# Output: Commit IDs, authors, messages, change counts, URLs

# Get commits from specific project and branch
commits = get_git_commits_tool("my-app", "develop", top=5, project="SpecificProject")
print(commits)

# Get detailed information about a specific commit
commit_details = get_git_commit_details_tool("my-app", "abc123def456")
print(commit_details)
# Output: Full commit message, author/committer info, file changes, summary
```

#### Pull Request Management

```python
from azuredevops_tools.tools import (
    get_pull_requests_tool,
    get_pull_request_details_tool,
    create_pull_request_tool,
    get_pull_request_policies_tool
)

# Get active pull requests (default status='active', top=20)
active_prs = get_pull_requests_tool("my-app", status="active")
print(active_prs)
# Output: PR list with IDs, titles, status, authors, reviewers, branch info

# Get pull requests targeting main branch
main_prs = get_pull_requests_tool("my-app", target_branch="main")
print(main_prs)

# Get completed PRs from specific project
completed_prs = get_pull_requests_tool("my-app", status="completed", 
                                       top=10, project="MyProject")
print(completed_prs)

# Get detailed information about a specific PR
pr_details = get_pull_request_details_tool("my-app", 123)
print(pr_details)
# Output: Full description, reviewers with votes, linked work items, merge status

# Create a new pull request with reviewers
new_pr = create_pull_request_tool(
    repository_id="my-app",
    title="Fix authentication bug",
    description="This PR fixes the authentication issue where users with special characters in passwords couldn't log in.",
    source_branch="feature/auth-fix",  # Without refs/heads/ prefix
    target_branch="main",
    reviewers=["reviewer1@company.com", "reviewer2@company.com"],
    is_draft=False,  # Set to True for draft PR
    project="MyProject"  # Optional project parameter
)
print(new_pr)
# Output: Created PR details with ID, URL, branch info

# Check branch policies and compliance for a PR
policies = get_pull_request_policies_tool("my-app", 123)
print(policies)
# Output: Policy names, status, evaluation times
```

#### Code Review and Approval Workflows

```python
from azuredevops_tools.tools import (
    approve_pull_request_tool,
    reject_pull_request_tool,
    request_pull_request_changes_tool
)

# Approve a pull request (vote = 10)
approval = approve_pull_request_tool("my-app", 123, "reviewer@company.com")
print(approval)
# Output: Confirmation with reviewer name, vote description, PR info

# Request changes on a pull request (vote = -5, "Waiting for Author")
changes = request_pull_request_changes_tool("my-app", 123, "reviewer@company.com")
print(changes)
# Output: Change request confirmation with vote details

# Reject a pull request (vote = -10, "Rejected")
rejection = reject_pull_request_tool("my-app", 123, "reviewer@company.com")
print(rejection)
# Output: Rejection confirmation with reviewer and vote info

# Multi-project approval workflow
approval_projectA = approve_pull_request_tool("my-app", 123, "reviewer@company.com", 
                                              project="ProjectA")
approval_projectB = approve_pull_request_tool("other-app", 456, "reviewer@company.com",
                                              project="ProjectB")
```

#### Complete Workflow Example

```python
# Multi-Project DevOps Analysis Workflow
from azuredevops_tools.tools import *

# 1. Organization-wide Project Discovery
all_projects = get_projects_tool()
print(f"Found {len(all_projects)} projects in organization")

# 2. Cross-Project Repository Analysis
for project_name in ["ProjectA", "ProjectB", "ProjectC"]:
    print(f"\n=== Analyzing {project_name} ===")
    
    # Get repositories in each project
    repos = get_git_repositories_tool(project=project_name)
    print(f"Repositories in {project_name}: {len(repos)}")
    
    # Analyze recent commits across repositories
    for repo_info in repos:
        repo_name = repo_info['name']
        commits = get_git_commits_tool(repo_name, top=5, project=project_name)
        print(f"  {repo_name}: {len(commits)} recent commits")

# 3. Build Health Analysis Across Projects
def analyze_build_health(project_name, pipeline_id=None):
    """Analyze build health for a project"""
    print(f"\n--- Build Health for {project_name} ---")
    
    # Get recent builds
    recent_builds = get_builds_tool(
        definition_id=pipeline_id, 
        top=10, 
        status_filter="completed", 
        project=project_name
    )
    
    # Analyze failed builds
    failed_builds = [b for b in recent_builds if 'failed' in b.lower()]
    if failed_builds:
        print(f"Found {len(failed_builds)} failed builds")
        
        # Get detailed failure info for the most recent failed build
        # Extract build ID from the failed build info and analyze
        latest_failed_id = extract_build_id(failed_builds[0])  # Custom helper
        failed_tasks = get_failed_tasks_with_logs_tool(latest_failed_id, project=project_name)
        print(f"Failed tasks analysis: {len(failed_tasks)} failed tasks found")
    
    return {
        'total_builds': len(recent_builds),
        'failed_builds': len(failed_builds),
        'success_rate': (len(recent_builds) - len(failed_builds)) / len(recent_builds) * 100
    }

# Analyze builds for multiple projects
build_health = {}
for project in ["ProjectA", "ProjectB"]:
    build_health[project] = analyze_build_health(project)

# 4. Pull Request Management Workflow
def manage_pull_requests(repo_name, project_name):
    """Complete PR management workflow"""
    print(f"\n--- PR Management for {repo_name} in {project_name} ---")
    
    # Get active PRs
    active_prs = get_pull_requests_tool(repo_name, status="active", project=project_name)
    print(f"Active PRs: {len(active_prs)}")
    
    for pr in active_prs:
        pr_id = pr['pullRequestId']
        
        # Get detailed PR information
        pr_details = get_pull_request_details_tool(repo_name, pr_id, project=project_name)
        
        # Check policy compliance
        policies = get_pull_request_policies_tool(repo_name, pr_id, project=project_name)
        
        # Automated approval logic (example)
        if all_policies_passed(policies) and has_required_approvals(pr_details):
            approval_result = approve_pull_request_tool(
                repo_name, pr_id, "automation@company.com", project=project_name
            )
            print(f"  Auto-approved PR #{pr_id}: {approval_result}")
        elif needs_changes(pr_details):
            change_request = request_pull_request_changes_tool(
                repo_name, pr_id, "reviewer@company.com", project=project_name
            )
            print(f"  Requested changes for PR #{pr_id}: {change_request}")

# Apply PR management to multiple repositories
for repo in ["web-app", "api-service", "data-processor"]:
    manage_pull_requests(repo, "ProjectA")

# 5. Changeset Analysis and Code Review
def analyze_recent_changes(project_name, author_name=None):
    """Analyze recent changesets for code review"""
    print(f"\n--- Recent Changes Analysis for {project_name} ---")
    
    # Get recent changesets
    changesets = get_changeset_list_tool(
        author=author_name, 
        from_changeset_id=50000,  # Last 1000 changesets
        to_changeset_id=51000,
        project=project_name
    )
    
    for changeset_info in changesets:
        changeset_id = extract_changeset_id(changeset_info)  # Custom helper
        
        # Get detailed changes
        changes = get_changeset_changes_tool(changeset_id, project=project_name)
        print(f"  Changeset {changeset_id}: {changes}")
        
        # Get file diffs for important files
        important_files = extract_important_files(changes)  # Custom helper
        for file_path in important_files:
            diff = get_file_diff_tool(file_path, changeset_id, project=project_name)
            print(f"    Diff for {file_path}: {len(diff)} characters")

# Analyze changes for specific developers
analyze_recent_changes("ProjectA", author_name="John Doe")
analyze_recent_changes("ProjectB", author_name="Jane Smith")

# 6. Cross-Project Comparison Report
def generate_comparison_report():
    """Generate a comprehensive cross-project comparison"""
    report = {
        'projects': {},
        'summary': {}
    }
    
    for project in ["ProjectA", "ProjectB", "ProjectC"]:
        project_data = {
            'repositories': len(get_git_repositories_tool(project=project)),
            'pipelines': len(get_build_pipelines_tool(project=project)),
            'recent_builds': len(get_builds_tool(top=50, project=project)),
            'active_prs': len(get_pull_requests_tool("main-repo", status="active", project=project))
        }
        report['projects'][project] = project_data
    
    # Calculate summary statistics
    report['summary'] = {
        'total_repositories': sum(p['repositories'] for p in report['projects'].values()),
        'total_pipelines': sum(p['pipelines'] for p in report['projects'].values()),
        'total_recent_builds': sum(p['recent_builds'] for p in report['projects'].values()),
        'average_prs_per_project': sum(p['active_prs'] for p in report['projects'].values()) / len(report['projects'])
    }
    
    return report

final_report = generate_comparison_report()
print(f"\n=== Final Cross-Project Report ===")
print(f"Total repositories across all projects: {final_report['summary']['total_repositories']}")
print(f"Total pipelines: {final_report['summary']['total_pipelines']}")
print(f"Total recent builds: {final_report['summary']['total_recent_builds']}")
print(f"Average PRs per project: {final_report['summary']['average_prs_per_project']:.1f}")
```

## 🔍 Tool Categories

### Changeset Tools (4 tools)
- **Purpose**: Analyze code modifications and version history in TFVC repositories
- **Key Features**: File diffs, change summaries, author filtering, ID range filtering
- **Best For**: Code review, change impact analysis, audit trails, developer activity tracking
- **Tools**: `get_changeset_tool`, `get_file_diff_tool`, `get_changeset_changes_tool`, `get_changeset_list_tool`

### Build Tools (4 tools)  
- **Purpose**: Monitor build execution, results, and analyze build logs
- **Key Features**: Status tracking, log analysis with preview/full content, timing information, filtering
- **Best For**: CI/CD monitoring, build failure investigation, build history analysis
- **Tools**: `get_build_tool`, `get_builds_tool`, `get_build_logs_tool`, `get_build_log_full_content_tool`

### Pipeline Tools (1 tool)
- **Purpose**: Manage build definitions and pipeline configurations  
- **Key Features**: Pipeline discovery, metadata retrieval, queue status
- **Best For**: Pipeline administration, configuration management, pipeline inventory
- **Tools**: `get_build_pipelines_tool`

### Diagnostic Tools (1 tool)
- **Purpose**: Troubleshoot build failures and identify issues quickly
- **Key Features**: Failed task identification, log extraction (last 200 lines), markdown formatting
- **Best For**: Problem diagnosis, failure analysis, debugging, troubleshooting workflows
- **Tools**: `get_failed_tasks_with_logs_tool`

### Git Repository Tools (4 tools)
- **Purpose**: Discover and analyze Git repositories, commits, and development activity
- **Key Features**: Repository metadata, commit history, change statistics, branch analysis
- **Best For**: Repository management, commit analysis, developer activity tracking, code archaeology
- **Tools**: `get_git_repositories_tool`, `get_git_repository_tool`, `get_git_commits_tool`, `get_git_commit_details_tool`

### Pull Request Tools (4 tools)
- **Purpose**: Manage pull requests, code reviews, and collaboration workflows
- **Key Features**: PR filtering, detailed information, creation workflow, policy compliance
- **Best For**: Code review management, PR automation, collaboration workflows, policy enforcement
- **Tools**: `get_pull_requests_tool`, `get_pull_request_details_tool`, `create_pull_request_tool`, `get_pull_request_policies_tool`

### Approval Workflow Tools (3 tools)
- **Purpose**: Handle code review votes and approval processes
- **Key Features**: Vote casting (approve/reject/request changes), reviewer management, automated workflows
- **Best For**: Automated approvals, code review automation, quality gates, review process management
- **Tools**: `approve_pull_request_tool`, `reject_pull_request_tool`, `request_pull_request_changes_tool`

### Project Management Tools (1 tool)
- **Purpose**: Discover and manage Azure DevOps projects across the organization
- **Key Features**: Project metadata, visibility settings, state information
- **Best For**: Organization management, project discovery, multi-project workflows
- **Tools**: `get_projects_tool`

**Total: 22 Tools** across 8 categories, all supporting optional project parameter for multi-project scenarios.

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
