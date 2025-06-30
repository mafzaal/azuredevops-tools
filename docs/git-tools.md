# Git Tools for Azure DevOps

This document describes the Git-related tools available in the Azure DevOps Tools package. These tools provide comprehensive support for Git repository management, commit analysis, pull request workflows, and approval processes.

## Overview

The Git tools are designed to integrate seamlessly with Azure DevOps Git repositories and provide LLM-friendly interfaces for common Git operations including:

- **Repository Management**: Discover and analyze Git repositories
- **Commit Analysis**: Examine commit history and changes
- **Pull Request Workflows**: Create, review, and manage pull requests
- **Approval Processes**: Handle code review and approval workflows
- **Policy Compliance**: Check branch policies and requirements

## Repository Tools

### `get_git_repositories_tool(project=None)`

Retrieves all Git repositories in the project with comprehensive metadata.

**Parameters:**
- `project` (str, optional): Azure DevOps project name

**Returns:** Formatted list of repositories with details including:
- Repository name and ID
- Default branch
- Size and URLs (remote, SSH, web)
- Status (active/disabled)
- Fork information

**Example:**
```python
from azuredevops_tools.tools import get_git_repositories_tool

# Get all repositories
repos = get_git_repositories_tool()
print(repos)
```

### `get_git_repository_tool(repository_id, project=None)`

Gets detailed information about a specific repository.

**Parameters:**
- `repository_id` (str): Repository ID or name
- `project` (str, optional): Azure DevOps project name

**Example:**
```python
repo_details = get_git_repository_tool("my-app")
```

## Commit Analysis Tools

### `get_git_commits_tool(repository_id, branch=None, top=10, project=None)`

Retrieves recent commits with author, message, and change statistics.

**Parameters:**
- `repository_id` (str): Repository ID or name
- `branch` (str, optional): Branch name (uses default branch if not specified)
- `top` (int): Maximum commits to retrieve (default: 10)
- `project` (str, optional): Azure DevOps project name

**Example:**
```python
# Get last 5 commits from main branch
commits = get_git_commits_tool("my-app", "main", 5)
```

### `get_git_commit_details_tool(repository_id, commit_id, project=None)`

Gets comprehensive details about a specific commit including file changes.

**Parameters:**
- `repository_id` (str): Repository ID or name
- `commit_id` (str): Commit SHA (can be abbreviated)
- `project` (str, optional): Azure DevOps project name

**Example:**
```python
commit_details = get_git_commit_details_tool("my-app", "abc123def456")
```

## Pull Request Tools

### `get_pull_requests_tool(repository_id, status='active', target_branch=None, source_branch=None, top=20, project=None)`

Retrieves pull requests with filtering options.

**Parameters:**
- `repository_id` (str): Repository ID or name
- `status` (str): Filter by status ('active', 'completed', 'abandoned', 'all')
- `target_branch` (str, optional): Filter by target branch
- `source_branch` (str, optional): Filter by source branch
- `top` (int): Maximum PRs to retrieve (default: 20)
- `project` (str, optional): Azure DevOps project name

**Example:**
```python
# Get active PRs targeting main branch
active_prs = get_pull_requests_tool("my-app", "active", target_branch="main")
```

### `get_pull_request_details_tool(repository_id, pull_request_id, project=None)`

Gets comprehensive details about a specific pull request.

**Parameters:**
- `repository_id` (str): Repository ID or name
- `pull_request_id` (int): Pull request ID number
- `project` (str, optional): Azure DevOps project name

**Returns:** Detailed PR information including:
- Title, description, and status
- Creator and creation date
- Source and target branches
- Reviewers and their votes
- Linked work items
- Labels and merge status

**Example:**
```python
pr_details = get_pull_request_details_tool("my-app", 123)
```

## Pull Request Creation

### `create_pull_request_tool(repository_id, title, description, source_branch, target_branch, reviewers=None, is_draft=False, project=None)`

Creates a new pull request with specified details and reviewers.

**Parameters:**
- `repository_id` (str): Repository ID or name
- `title` (str): Pull request title
- `description` (str): Pull request description
- `source_branch` (str): Source branch name (without refs/heads/)
- `target_branch` (str): Target branch name (without refs/heads/)
- `reviewers` (List[str], optional): List of reviewer IDs, emails, or display names
- `is_draft` (bool): Create as draft PR (default: False)
- `project` (str, optional): Azure DevOps project name

**Example:**
```python
new_pr = create_pull_request_tool(
    repository_id="my-app",
    title="Fix authentication bug",
    description="This PR fixes the authentication issue...",
    source_branch="feature/auth-fix",
    target_branch="main",
    reviewers=["john@company.com", "jane@company.com"],
    is_draft=False
)
```

## Pull Request Approval Tools

### `approve_pull_request_tool(repository_id, pull_request_id, reviewer_id, project=None)`

Approves a pull request by casting an approval vote (vote value: 10).

**Parameters:**
- `repository_id` (str): Repository ID or name
- `pull_request_id` (int): Pull request ID number
- `reviewer_id` (str): Reviewer's ID, email, or unique name
- `project` (str, optional): Azure DevOps project name

**Example:**
```python
approval = approve_pull_request_tool("my-app", 123, "john@company.com")
```

### `reject_pull_request_tool(repository_id, pull_request_id, reviewer_id, project=None)`

Rejects a pull request by casting a rejection vote (vote value: -10).

**Example:**
```python
rejection = reject_pull_request_tool("my-app", 123, "john@company.com")
```

### `request_pull_request_changes_tool(repository_id, pull_request_id, reviewer_id, project=None)`

Requests changes on a pull request by casting a "waiting for author" vote (vote value: -5).

**Example:**
```python
changes = request_pull_request_changes_tool("my-app", 123, "john@company.com")
```

## Policy and Compliance Tools

### `get_pull_request_policies_tool(repository_id, pull_request_id, project=None)`

Gets branch policies and their evaluation status for a pull request.

**Parameters:**
- `repository_id` (str): Repository ID or name
- `pull_request_id` (int): Pull request ID number
- `project` (str, optional): Azure DevOps project name

**Returns:** Information about:
- Policy names and types
- Evaluation status (approved, running, failed)
- Start and completion times
- Policy configuration details

**Example:**
```python
policies = get_pull_request_policies_tool("my-app", 123)
```

## Vote Values Reference

Azure DevOps uses the following vote values for pull request reviews:

| Vote Value | Description | Tool Function |
|------------|-------------|---------------|
| 10 | Approved | `approve_pull_request_tool()` |
| 5 | Approved with Suggestions | (manual vote) |
| 0 | No Vote | (default state) |
| -5 | Waiting for Author | `request_pull_request_changes_tool()` |
| -10 | Rejected | `reject_pull_request_tool()` |

## Common Workflow Examples

### Code Review Workflow

```python
# 1. Create a pull request
new_pr = create_pull_request_tool(
    "my-app", 
    "Feature: Add user authentication",
    "Implements JWT-based authentication system",
    "feature/auth",
    "main",
    ["reviewer1@company.com", "reviewer2@company.com"]
)

# 2. Get PR details for review
pr_details = get_pull_request_details_tool("my-app", new_pr['pullRequestId'])

# 3. Check commits in the PR
commits = get_git_commits_tool("my-app", "feature/auth", 10)

# 4. Approve the PR
approval = approve_pull_request_tool("my-app", new_pr['pullRequestId'], "reviewer1@company.com")

# 5. Check policy compliance
policies = get_pull_request_policies_tool("my-app", new_pr['pullRequestId'])
```

### Repository Audit

```python
# 1. Get all repositories
repos = get_git_repositories_tool()

# 2. For each repo, check recent activity
for repo in repos:
    print(f"Repository: {repo['name']}")
    
    # Get recent commits
    commits = get_git_commits_tool(repo['name'], top=5)
    
    # Get active pull requests
    prs = get_pull_requests_tool(repo['name'], "active")
    
    print(f"Recent commits: {len(commits)}")
    print(f"Active PRs: {len(prs)}")
```

### Release Management

```python
# 1. Get commits since last release
recent_commits = get_git_commits_tool("my-app", "main", 50)

# 2. Analyze commits for release notes
for commit in recent_commits:
    commit_details = get_git_commit_details_tool("my-app", commit['commitId'])
    # Process commit for release notes

# 3. Create release PR
release_pr = create_pull_request_tool(
    "my-app",
    "Release v2.1.0",
    "Release notes:\n- Feature A\n- Bug fix B\n- Performance improvements",
    "release/v2.1.0",
    "main",
    ["release-manager@company.com"]
)
```

## Error Handling

All tools include comprehensive error handling and return descriptive error messages:

```python
try:
    pr_details = get_pull_request_details_tool("invalid-repo", 999)
    print(pr_details)
except Exception as e:
    print(f"Error: {e}")
```

Error messages include:
- Repository not found
- Pull request not found  
- Permission denied
- Network connectivity issues
- Invalid parameters

## Environment Setup

Before using the Git tools, ensure you have configured:

```bash
export DEVOPS_PAT="your-personal-access-token"
export DEVOPS_ORGANIZATION="your-organization"
export DEVOPS_PROJECT="your-project"
```

The Personal Access Token should have permissions for:
- Code (read/write)
- Pull Request (read/write)
- Project and Team (read)

## Integration with LLMs

These tools are designed for optimal LLM integration:

- **Descriptive function names** that clearly indicate functionality
- **Comprehensive docstrings** with examples and parameter descriptions
- **Structured return values** that are easy to parse and understand
- **Consistent error handling** with informative messages
- **Optional project parameters** for multi-project scenarios

## Best Practices

1. **Use specific repository IDs** rather than names when possible for better performance
2. **Limit result sets** using the `top` parameter to avoid overwhelming responses
3. **Check policy compliance** before attempting to complete pull requests
4. **Use draft PRs** for work-in-progress changes
5. **Include descriptive PR titles and descriptions** for better collaboration
6. **Verify reviewer permissions** before assigning reviews

## See Also

- [Azure DevOps REST API Documentation](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- [Git Workflow Best Practices](https://docs.microsoft.com/en-us/azure/devops/repos/git/)
- [Branch Policies](https://docs.microsoft.com/en-us/azure/devops/repos/git/branch-policies/)
