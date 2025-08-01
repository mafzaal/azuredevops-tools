"""
Azure DevOps Tools Module for LLM/MCP Integration
 
This module provides a collection of MCP-compatible tools for interacting with Azure DevOps.
It includes tools for changesets, builds, pipelines, and code analysis that can be easily
discovered and used by Large Language Models through the Model Context Protocol (MCP).

Each tool follows MCP naming conventions and includes comprehensive documentation for
optimal LLM discoverability and usage. All tools support an optional 'project' parameter
to allow targeting specific Azure DevOps projects, while defaulting to the configured project.

Tool Categories:
- Changeset Tools: Retrieve and analyze code changes
- Build Tools: Monitor and analyze build results  
- Pipeline Tools: Manage and inspect CI/CD pipelines
- Diagnostic Tools: Debug failed builds and tasks

Project Parameter:
All tools accept an optional 'project' parameter (str) to specify the Azure DevOps project.
If not provided, the tools will use the default project configured in the DevOpsToolset instance.
This allows the same tool instance to work with multiple projects when needed.
"""


from .devops_tools import DevOpsToolset
from typing import Dict, Any, Optional, List
import logging


# Initialize DevOps toolset
devops = DevOpsToolset()


def get_changeset_tool(changeset_id: int, project: Optional[str] = None) -> str:
    """
    Get a specific changeset and summarize its details.
    
    This tool retrieves detailed information about a specific changeset from Azure DevOps,
    including the changeset ID, commit comment, author information, and creation timestamp.
    
    Parameters:
        changeset_id (int): The ID of the changeset to retrieve.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
        
    Returns:
        str: A formatted summary of the changeset with ID, comment, author, and date.
        
    Example:
        get_changeset_tool(12345)
    Output:
        "Changeset 12345 - Initial commit by John Doe on 2023-10-01T12:00:00.000Z"
    """
    try:
        changeset = devops.get_changeset(changeset_id, project=project)
        
        if not changeset:
            return f"Changeset {changeset_id} not found or could not be retrieved."
        
        changeset_id_str = changeset.get('changesetId', changeset_id)
        comment = changeset.get('comment', 'No comment')
        author_info = changeset.get('author', {})
        author_name = author_info.get('displayName', 'Unknown') if author_info else 'Unknown'
        created_date = changeset.get('createdDate', 'Unknown date')
        
        return f"Changeset {changeset_id_str} - {comment} by {author_name} on {created_date}"
        
    except Exception as e:
        logging.error(f"Error retrieving changeset {changeset_id}: {e}")
        return f"Error retrieving changeset {changeset_id}: {str(e)}"

def get_file_diff_tool(file_path: str, changeset_id: int, project: Optional[str] = None) -> str:
    """
    Get the file diff for a specific file in a changeset.
    
    This tool retrieves the detailed diff/changes for a specific file within a given changeset,
    showing the line-by-line differences compared to the previous version. This is useful for
    code review, understanding changes, and analyzing modifications.
    
    Parameters:
        file_path (str): The full path of the file to get the diff for (e.g., "src/main.py").
        changeset_id (int): The ID of the changeset containing the file changes.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
        
    Returns:
        str: The formatted diff showing additions, deletions, and modifications, or an error message.
        
    Example:
        get_file_diff_tool("src/main.py", 12345)
    Output:
        "File diff for src/main.py in changeset 12345:
         --- src/main.py
         +++ src/main.py
         @@ -1,3 +1,3 @@
         -print('Hello, World!')
         +print('Hello, DevOps!')"
    """
    try:
        diff = devops.get_file_diff(file_path, changeset_id, project=project)
        return f"File diff for {file_path} in changeset {changeset_id}:\n{diff}"
    except Exception as e:
        logging.error(f"Error getting file diff for {file_path} in changeset {changeset_id}: {e}")
        return f"Error getting file diff for {file_path} in changeset {changeset_id}: {str(e)}"
    

def get_changeset_changes_tool(changeset_id: int, project: Optional[str] = None) -> str:
    """
    Get changes for a specific changeset and summarize them.
    
    This tool retrieves and summarizes all file changes within a specific changeset,
    showing which files were added, modified, deleted, or renamed. Binary files are
    excluded from the summary to focus on code changes.
    
    Parameters:
        changeset_id (int): The ID of the changeset to retrieve changes for.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
        
    Returns:
        str: A formatted summary of all file changes in the changeset, excluding binary files.
        
    Example:
        get_changeset_changes_tool(12345)
    Output:
        "Changeset 12345 has 2 file(s) changed:
         - src/main.py (Modified)
         - src/utils.py (Added)"
    """
    changes = devops.get_changeset_changes(changeset_id, project=project)
    
    if not changes:
        return f"No changes found for changeset {changeset_id}."
    
    changes_summary = []
    
    for change in changes:
        file_path = change.get('path', 'Unknown path')
        change_type = change.get('changeType', 'Unknown change type')
        
        # Get file diff for context
        if not file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico')):
            changes_summary.append(f"- {file_path} ({change_type})")
    
    return  f"Changeset {changeset_id} has {len(changes_summary)} file(s) changed:\n" + "\n".join(changes_summary) if changes_summary else "No significant file changes found."

def get_changeset_list_tool(author: Optional[str] = None, from_changeset_id: Optional[int] = None, to_changeset_id: Optional[int] = None, project: Optional[str] = None) -> str:
    """
    Get a list of changesets optionally filtered by author and/or changeset ID range.
    
    This tool retrieves multiple changesets from Azure DevOps with optional filtering
    capabilities. You can filter by author name and/or specify a range of changeset IDs
    to narrow down the results. Useful for analyzing recent changes or specific developer contributions.
    
    Parameters:
        author (str, optional): The display name of the author to filter changesets by.
        from_changeset_id (int, optional): The starting changeset ID for the range filter.
        to_changeset_id (int, optional): The ending changeset ID for the range filter.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: A formatted list of changesets with IDs, comments, authors, and creation dates.
    
    Example:
        get_changeset_list_tool(author="John Doe", from_changeset_id=12340, to_changeset_id=12350)
    Output:
        "Found 2 changesets:
         Changeset 12345 - Initial commit by John Doe on 2023-10-01T12:00:00.000Z
         Changeset 12346 - Fix bug #123 by John Doe on 2023-10-02T14:30:00.000Z"
    """
    try:
        changesets = devops.get_changeset_list(author, from_changeset_id, to_changeset_id, project=project)
        
        if not changesets:
            return f"No changesets found matching the criteria."
        
        changesets_summary = [f"Found {len(changesets)} changesets:"]
        
        for changeset in changesets:
            author_info = changeset.get('author', {})
            author_name = author_info.get('displayName', 'Unknown') if author_info else 'Unknown'
            changesets_summary.append(
                f"Changeset {changeset.get('changesetId')} - {changeset.get('comment', 'No comment')} "
                f"by {author_name} on {changeset.get('createdDate', 'Unknown date')}"
            )
        
        return "\n".join(changesets_summary)
    except Exception as e:
        logging.error(f"Error getting changeset list: {e}")
        return f"Error getting changeset list: {str(e)}"

def get_build_tool(build_id: int, project: Optional[str] = None) -> str:
    """
    Get detailed information about a specific build.
    
    This tool retrieves comprehensive information about a specific Azure DevOps build,
    including its current status, result, duration, requester, and build definition details.
    Essential for monitoring build progress and diagnosing build issues.
    
    Parameters:
        build_id (int): The unique ID of the build to retrieve information for.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: A detailed summary of the build including status, result, timing, and metadata.
    
    Example:
        get_build_tool(12345)
    Output:
        "Build 12345 (20230601.1):
         Status: completed
         Result: succeeded
         Requested by: John Doe
         Duration: 00:15:32"
    """
    try:
        return devops.f1e_get_build_tool(build_id, project=project)
    except Exception as e:
        logging.error(f"Error getting build {build_id}: {e}")
        return f"Error getting build {build_id}: {str(e)}"

def get_builds_tool(definition_id: Optional[int] = None, top: int = 50, status_filter: Optional[str] = None, project: Optional[str] = None) -> str:
    """
    Get a list of builds from Azure DevOps with optional filtering.
    
    This tool retrieves multiple builds from Azure DevOps with filtering capabilities.
    You can filter by specific pipeline/definition ID, limit the number of results,
    and filter by build status. Useful for monitoring recent builds and analyzing patterns.
    
    Parameters:
        definition_id (int, optional): Filter builds by specific pipeline/definition ID.
        top (int): Maximum number of builds to retrieve (default: 50).
        status_filter (str, optional): Filter by status ('completed', 'inProgress', 'notStarted').
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: A formatted list of builds with IDs, statuses, results, and timing information.
    
    Example:
        get_builds_tool(definition_id=139, top=10, status_filter="completed")
    Output:
        "Found 10 build(s):
        
        Build 12345 (20230601.1):
          Status: completed
          Result: succeeded
          Requested by: John Doe
          Pipeline: D365FnO - Build (ID: 139)
          Start time: 2023-10-01T12:00:00.000Z
          Finish time: 2023-10-01T12:15:00.000Z
          Duration: 0:15:00"
    """
    try:
        return devops.f1e_get_builds_tool(definition_id, top, status_filter, project=project)
    except Exception as e:
        logging.error(f"Error getting builds: {e}")
        return f"Error getting builds: {str(e)}"

def get_build_logs_tool(build_id: int, project: Optional[str] = None) -> Dict[str, Any]:
    """
    Get logs summary for a specific build with preview content (first 50 lines).
    
    This tool retrieves a structured overview of all logs for a specific build,
    including metadata and preview content (first 50 lines) for each log.
    Essential for quickly understanding build output and identifying issues.
    
    Parameters:
        build_id (int): The unique ID of the build to retrieve logs for.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        Dict[str, Any]: A structured dictionary containing build logs with metadata and preview content.
                       Includes buildId, totalLogs count, and detailed log information with
                       preview content, line counts, and hasMoreContent flags.
    
    Example:
        get_build_logs_tool(12345)
    Output:
        {
            'buildId': 12345,
            'totalLogs': 2,
            'logs': [
                {
                    'id': 1,
                    'type': 'Console',
                    'url': 'https://...',
                    'createdOn': '2023-10-01T12:00:00.000Z',
                    'lastChangedOn': '2023-10-01T12:15:00.000Z',
                    'contentLines': ['##[section]Starting: Build', '##[section]Starting: Initialize Job', ...],
                    'contentLineCount': 256,
                    'previewContent': '##[section]Starting: Build\n##[section]Starting: Initialize Job\n...',
                    'hasMoreContent': true
                }
            ]
        }
    """
    try:
        return devops.f1e_get_build_logs_tool(build_id, project=project)
    except Exception as e:
        logging.error(f"Error getting build logs for build {build_id}: {e}")
        return {
            'buildId': build_id,
            'error': str(e),
            'logs': []
        }

def get_build_log_full_content_tool(build_id: int, log_id: int, project: Optional[str] = None) -> str:
    """
    Get the full content of a specific build log.
    
    This tool retrieves the complete, untruncated content of a specific log within a build.
    Returns the content formatted as markdown with metadata and full log content.
    Use this when you need to see the complete log details beyond the preview.
    
    Parameters:
        build_id (int): The unique ID of the build containing the log.
        log_id (int): The unique ID of the specific log to retrieve full content for.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: A markdown-formatted string containing complete log content and metadata.
    
    Example:
        get_build_log_full_content_tool(12345, 1)
    Output:
        # Build Log 12345 - Log 1
        
        ## Log Metadata
        - **Type**: Console
        - **Created**: 2023-10-01T12:00:00.000Z
        - **Last Changed**: 2023-10-01T12:15:00.000Z
        - **Total Lines**: 256
        
        ## Log Content
        ```
        ##[section]Starting: Build
        ##[section]Starting: Initialize Job
        ...
        ```
    """
    try:
        log_data = devops.f1e_get_build_log_full_content_tool(build_id, log_id, project=project)
        
        if 'error' in log_data:
            return f"# Build Log {build_id} - Log {log_id}\n\n**Error**: {log_data['error']}"
        
        markdown_content = f"# Build Log {build_id} - Log {log_id}\n\n"
        
        # Add metadata section
        if 'logMetadata' in log_data:
            metadata = log_data['logMetadata']
            markdown_content += "## Log Metadata\n"
            markdown_content += f"- **Type**: {metadata.get('type', 'Unknown')}\n"
            markdown_content += f"- **Created**: {metadata.get('createdOn', 'Unknown')}\n"
            markdown_content += f"- **Last Changed**: {metadata.get('lastChangedOn', 'Unknown')}\n"
            markdown_content += f"- **Total Lines**: {log_data.get('contentLineCount', 0)}\n\n"
        
        # Add log content section
        markdown_content += "## Log Content\n"
        markdown_content += "```\n"
        markdown_content += log_data.get('fullContent', '')
        markdown_content += "\n```\n"
        
        return markdown_content
        
    except Exception as e:
        logging.error(f"Error getting full content for log {log_id} in build {build_id}: {e}")
        return f"# Build Log {build_id} - Log {log_id}\n\n**Error**: {str(e)}"

def get_failed_tasks_with_logs_tool(build_id: int, project: Optional[str] = None) -> str:
    """
    Get failed tasks for a build and the last 200 lines of their logs.
    
    This diagnostic tool specifically identifies failed tasks within a build and retrieves
    the last 200 lines of their logs for troubleshooting. Essential for quickly identifying
    and diagnosing build failures without reviewing entire logs.
    
    Parameters:
        build_id (int): The unique ID of the build to analyze for failed tasks.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
        
    Returns:
        str: A markdown-formatted string containing failed task details and their recent log content.
        
    Example:
        get_failed_tasks_with_logs_tool(12345)
    Output:
        # Failed Tasks for Build 12345
        
        ## Task: Build (Log ID: 7)
        ```
        line1
        line2
        ...
        ```
        
        ## Task: Test (Log ID: 9)
        ```
        test line1
        test line2
        ...
        ```
    """
    try:
        failed_tasks = devops.get_failed_tasks_with_logs(build_id, project=project)
        
        if not failed_tasks:
            return f"# Failed Tasks for Build {build_id}\n\nNo failed tasks found for this build."
        
        markdown_content = f"# Failed Tasks for Build {build_id}\n\n"
        
        for task in failed_tasks:
            task_name = task.get('taskName', 'Unknown Task')
            log_id = task.get('logId', 'Unknown')
            log_lines = task.get('last200LogLines', [])
            
            markdown_content += f"## Task: {task_name} (Log ID: {log_id})\n\n"
            
            if log_lines:
                markdown_content += "```\n"
                markdown_content += '\n'.join(log_lines)
                markdown_content += "\n```\n\n"
            else:
                markdown_content += "*No log content available*\n\n"
        
        return markdown_content.rstrip()  # Remove trailing whitespace
        
    except Exception as e:
        logging.error(f"Error getting failed tasks/logs for build {build_id}: {e}")
        return f"# Failed Tasks for Build {build_id}\n\n**Error**: {str(e)}"

def get_build_pipelines_tool(project: Optional[str] = None) -> str:
    """
    Get a list of all build pipelines/definitions in the project.
    
    This tool retrieves comprehensive information about all available build pipelines
    in the Azure DevOps project, including their IDs, names, types, revision information,
    queue status, and repository details. Essential for pipeline management and discovery.
    
    Parameters:
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: A formatted string with detailed information about all build pipelines.
    
    Example:
        get_build_pipelines_tool()
    Output:
        "Found 3 build pipeline(s):
        
        Pipeline ID: 1
        Name: CI/CD Pipeline
        Type: build
        Quality: definition
        Revision: 5
        Queue Status: enabled
        Created: 2023-10-01T12:00:00.000Z
        Authored by: John Doe
        Repository: my-repo (Git)
        URL: https://dev.azure.com/...
        ------------------------------------------------------------"
    """
    try:
        return devops.f1e_get_build_pipelines_tool(project=project)
    except Exception as e:
        logging.error(f"Error getting build pipelines: {e}")
        return f"Error getting build pipelines: {str(e)}"


# Project Tools
def get_projects_tool() -> str:
    """
    Get a list of all projects in the Azure DevOps organization.
    
    This tool retrieves comprehensive information about all projects in the
    Azure DevOps organization, including project names, IDs, descriptions, state,
    visibility, and last update time. Essential for project discovery and management.
    
    Returns:
        str: A formatted list of projects with detailed information.
    
    Example:
        get_projects_tool()
    Output:
        "Found 3 projects in the organization:
        
        Project: MyProject
        ID: abc123-def456-ghi789
        Description: Main application project
        State: wellFormed
        Visibility: private
        Last Updated: 2023-10-01T12:00:00.000Z
        URL: https://dev.azure.com/myorg/MyProject
        ------------------------------------------------------------"
    """
    try:
        projects = devops.get_projects()
        
        if not projects:
            return "No projects found in the organization."
        
        result = f"Found {len(projects)} project(s) in the organization:\n"
        
        for project in projects:
            result += f"\nProject: {project['name']}\n"
            result += f"ID: {project['id']}\n"
            if project['description']:
                result += f"Description: {project['description']}\n"
            result += f"State: {project['state']}\n"
            result += f"Visibility: {project['visibility']}\n"
            if project['lastUpdateTime']:
                result += f"Last Updated: {project['lastUpdateTime']}\n"
            result += f"URL: {project['url']}\n"
            result += "------------------------------------------------------------\n"
        
        return result
    except Exception as e:
        logging.error(f"Error getting projects: {e}")
        return f"Error getting projects: {str(e)}"


# Git Repository Tools
def get_git_repositories_tool(project: Optional[str] = None) -> str:
    """
    Get a list of all Git repositories in the Azure DevOps project.
    
    This tool retrieves comprehensive information about all Git repositories
    in the project, including repository names, URLs, default branches, and metadata.
    Essential for repository discovery and management.
    
    Parameters:
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: A formatted list of Git repositories with detailed information.
    
    Example:
        get_git_repositories_tool()
    Output:
        "Found 3 Git repositories:
        
        Repository: my-app
        ID: abc123-def456-ghi789
        Default Branch: refs/heads/main
        Size: 15.2 MB
        Remote URL: https://dev.azure.com/myorg/myproject/_git/my-app
        SSH URL: git@ssh.dev.azure.com:v3/myorg/myproject/my-app
        Web URL: https://dev.azure.com/myorg/myproject/_git/my-app
        Status: Active
        ------------------------------------------------------------"
    """
    try:
        repositories = devops.get_git_repositories(project=project)
        
        if not repositories:
            return "No Git repositories found in the project."
        
        result = f"Found {len(repositories)} Git repositories:\n\n"
        
        for repo in repositories:
            result += f"Repository: {repo['name']}\n"
            result += f"ID: {repo['id']}\n"
            if repo['defaultBranch']:
                result += f"Default Branch: {repo['defaultBranch']}\n"
            if repo['size']:
                size_mb = repo['size'] / (1024 * 1024)
                result += f"Size: {size_mb:.1f} MB\n"
            if repo['remoteUrl']:
                result += f"Remote URL: {repo['remoteUrl']}\n"
            if repo['sshUrl']:
                result += f"SSH URL: {repo['sshUrl']}\n"
            if repo['webUrl']:
                result += f"Web URL: {repo['webUrl']}\n"
            result += f"Status: {'Disabled' if repo['isDisabled'] else 'Active'}\n"
            if repo['isFork']:
                result += "Type: Fork\n"
            result += "-" * 60 + "\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting Git repositories: {e}")
        return f"Error getting Git repositories: {str(e)}"

def get_git_repository_tool(repository_id: str, project: Optional[str] = None) -> str:
    """
    Get detailed information about a specific Git repository.
    
    This tool retrieves comprehensive details about a specific Git repository,
    including metadata, branch information, and repository statistics.
    
    Parameters:
        repository_id (str): The repository ID or name.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: Detailed information about the specified repository.
    
    Example:
        get_git_repository_tool("my-app")
    Output:
        "Repository: my-app
         ID: abc123-def456-ghi789
         Default Branch: refs/heads/main
         Size: 15.2 MB
         Remote URL: https://dev.azure.com/myorg/myproject/_git/my-app
         Status: Active"
    """
    try:
        repository = devops.get_git_repository(repository_id, project=project)
        
        if not repository:
            return f"Repository '{repository_id}' not found."
        
        result = f"Repository: {repository['name']}\n"
        result += f"ID: {repository['id']}\n"
        if repository['defaultBranch']:
            result += f"Default Branch: {repository['defaultBranch']}\n"
        if repository['size']:
            size_mb = repository['size'] / (1024 * 1024)
            result += f"Size: {size_mb:.1f} MB\n"
        if repository['remoteUrl']:
            result += f"Remote URL: {repository['remoteUrl']}\n"
        if repository['sshUrl']:
            result += f"SSH URL: {repository['sshUrl']}\n"
        if repository['webUrl']:
            result += f"Web URL: {repository['webUrl']}\n"
        result += f"Status: {'Disabled' if repository['isDisabled'] else 'Active'}\n"
        if repository['isFork']:
            result += "Type: Fork\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting Git repository {repository_id}: {e}")
        return f"Error getting Git repository {repository_id}: {str(e)}"

def get_git_commits_tool(repository_id: str, branch: Optional[str] = None, 
                        top: int = 10, project: Optional[str] = None) -> str:
    """
    Get recent Git commits from a repository.
    
    This tool retrieves recent commits from a Git repository, showing commit messages,
    authors, dates, and change statistics. Useful for understanding recent development activity.
    
    Parameters:
        repository_id (str): The repository ID or name.
        branch (str, optional): The branch name. If not provided, uses default branch.
        top (int): Maximum number of commits to retrieve (default: 10).
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: A formatted list of recent commits with details.
    
    Example:
        get_git_commits_tool("my-app", "main", 5)
    Output:
        "Found 5 commits from repository my-app:
        
        Commit: abc123def456 (2023-10-01T12:00:00Z)
        Author: John Doe <john@example.com>
        Message: Fix bug in authentication module
        Changes: +15 -3 (18 total)
        URL: https://dev.azure.com/...
        ------------------------------------------------------------"
    """
    try:
        commits = devops.get_git_commits(repository_id, branch=branch, top=top, project=project)
        
        # Check if we got an error response
        if commits and len(commits) == 1 and isinstance(commits[0], dict) and commits[0].get('error'):
            error_info = commits[0]
            return f"Error retrieving commits from repository '{repository_id}': {error_info['error_message']}\n\nDetails: {error_info['error_details']}"
        
        if not commits:
            return f"No commits found in repository '{repository_id}'" + (f" on branch '{branch}'" if branch else "")
        
        result = f"Found {len(commits)} commits from repository {repository_id}"
        if branch:
            result += f" on branch '{branch}'"
        result += ":\n\n"
        
        for commit in commits:
            result += f"Commit: {commit['commitId']}"
            if commit['author'] and commit['author']['date']:
                result += f" ({commit['author']['date']})"
            result += "\n"
            
            if commit['author']:
                result += f"Author: {commit['author']['name']}"
                if commit['author']['email']:
                    result += f" <{commit['author']['email']}>"
                result += "\n"
            
            if commit['comment']:
                # Truncate long commit messages
                comment = commit['comment']
                if len(comment) > 100:
                    comment = comment[:97] + "..."
                result += f"Message: {comment}\n"
            
            if commit['changeCounts']:
                changes = commit['changeCounts']
                adds = changes.get('Add', 0)
                edits = changes.get('Edit', 0) 
                deletes = changes.get('Delete', 0)
                total = adds + edits + deletes
                result += f"Changes: +{adds} ~{edits} -{deletes} ({total} total)\n"
            
            if commit['url']:
                result += f"URL: {commit['url']}\n"
            
            result += "-" * 60 + "\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting Git commits from {repository_id}: {e}")
        return f"Error getting Git commits from {repository_id}: {str(e)}"

def get_git_commit_details_tool(repository_id: str, commit_id: str, 
                               project: Optional[str] = None) -> str:
    """
    Get detailed information about a specific Git commit.
    
    This tool retrieves comprehensive details about a specific commit, including
    the full commit message, author information, file changes, and modifications.
    
    Parameters:
        repository_id (str): The repository ID or name.
        commit_id (str): The commit SHA (can be abbreviated).
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: Detailed information about the specified commit.
    
    Example:
        get_git_commit_details_tool("my-app", "abc123def456")
    Output:
        "Commit: abc123def456789...
         Author: John Doe <john@example.com> (2023-10-01T12:00:00Z)
         Committer: John Doe <john@example.com> (2023-10-01T12:00:00Z)
         
         Message:
         Fix bug in authentication module
         
         This commit addresses the issue where users were unable to
         authenticate when using special characters in passwords.
         
         Changes:
         - src/auth/login.py (Edit)
         - tests/test_auth.py (Edit)
         - README.md (Edit)"
    """
    try:
        commit_details = devops.get_git_commit_details(repository_id, commit_id, project=project)
        
        if not commit_details:
            return f"Commit '{commit_id}' not found in repository '{repository_id}'"
        
        result = f"Commit: {commit_details['commitId']}\n"
        
        if commit_details['author']:
            author = commit_details['author']
            result += f"Author: {author['name']}"
            if author['email']:
                result += f" <{author['email']}>"
            if author['date']:
                result += f" ({author['date']})"
            result += "\n"
        
        if commit_details['committer']:
            committer = commit_details['committer']
            result += f"Committer: {committer['name']}"
            if committer['email']:
                result += f" <{committer['email']}>"
            if committer['date']:
                result += f" ({committer['date']})"
            result += "\n"
        
        if commit_details['comment']:
            result += f"\nMessage:\n{commit_details['comment']}\n"
        
        if commit_details['changes']:
            result += "\nChanges:\n"
            for change in commit_details['changes']:
                if change['item'] and change['item']['path']:
                    result += f"- {change['item']['path']} ({change['changeType']})\n"
        
        if commit_details['changeCounts']:
            changes = commit_details['changeCounts']
            adds = changes.get('Add', 0)
            edits = changes.get('Edit', 0)
            deletes = changes.get('Delete', 0)
            total = adds + edits + deletes
            result += f"\nSummary: +{adds} ~{edits} -{deletes} ({total} total changes)\n"
        
        if commit_details['url']:
            result += f"\nURL: {commit_details['url']}\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting Git commit details for {commit_id}: {e}")
        return f"Error getting Git commit details for {commit_id}: {str(e)}"

# Pull Request Tools
def get_pull_requests_tool(repository_id: str, status: str = 'active',
                          target_branch: Optional[str] = None, source_branch: Optional[str] = None,
                          top: int = 20, project: Optional[str] = None) -> str:
    """
    Get pull requests from a Git repository with filtering options.
    
    This tool retrieves pull requests from a repository with various filtering options.
    Shows PR status, authors, reviewers, and approval states for code review workflows.
    
    Parameters:
        repository_id (str): The repository ID or name.
        status (str): PR status filter ('active', 'completed', 'abandoned', 'all'). Default: 'active'.
        target_branch (str, optional): Filter by target branch name.
        source_branch (str, optional): Filter by source branch name.
        top (int): Maximum number of PRs to retrieve (default: 20).
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: A formatted list of pull requests with status and reviewer information.
    
    Example:
        get_pull_requests_tool("my-app", "active", "main")
    Output:
        "Found 3 active pull requests in repository my-app:
        
        PR #123: Fix authentication bug
        Status: Active (Draft)
        Created by: John Doe on 2023-10-01T12:00:00Z
        Source: feature/auth-fix → Target: main
        Reviewers: 
        - Jane Smith (Approved)
        - Bob Wilson (Waiting for Author)
        URL: https://dev.azure.com/...
        ------------------------------------------------------------"
    """
    try:
        pull_requests = devops.get_pull_requests(
            repository_id=repository_id,
            status=status,
            target_branch=target_branch,
            source_branch=source_branch,
            top=top,
            project=project
        )
        
        if not pull_requests:
            filter_desc = f"{status} pull requests"
            if target_branch:
                filter_desc += f" targeting '{target_branch}'"
            if source_branch:
                filter_desc += f" from '{source_branch}'"
            return f"No {filter_desc} found in repository '{repository_id}'"
        
        status_desc = status if status != 'all' else 'pull requests'
        result = f"Found {len(pull_requests)} {status_desc} in repository {repository_id}:\n\n"
        
        for pr in pull_requests:
            result += f"PR #{pr['pullRequestId']}: {pr['title']}\n"
            result += f"Status: {pr['status'].title()}"
            if pr['isDraft']:
                result += " (Draft)"
            result += "\n"
            
            if pr['createdBy']:
                result += f"Created by: {pr['createdBy']['displayName']}"
                if pr['creationDate']:
                    result += f" on {pr['creationDate']}"
                result += "\n"
            
            # Format branch names (remove refs/heads/ prefix)
            source_branch = pr['sourceRefName'].replace('refs/heads/', '') if pr['sourceRefName'] else 'unknown'
            target_branch = pr['targetRefName'].replace('refs/heads/', '') if pr['targetRefName'] else 'unknown'
            result += f"{source_branch} → {target_branch}\n"
            
            if pr['reviewers']:
                result += "Reviewers:\n"
                for reviewer in pr['reviewers']:
                    vote_desc = {
                        -10: "Rejected",
                        -5: "Waiting for Author",
                        0: "No Vote",
                        5: "Approved with Suggestions", 
                        10: "Approved"
                    }.get(reviewer['vote'], "Unknown")
                    
                    result += f"- {reviewer['displayName']} ({vote_desc})"
                    if reviewer['isRequired']:
                        result += " [Required]"
                    result += "\n"
            
            if pr['url']:
                result += f"URL: {pr['url']}\n"
            
            result += "-" * 60 + "\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting pull requests from {repository_id}: {e}")
        return f"Error getting pull requests from {repository_id}: {str(e)}"

def get_pull_request_details_tool(repository_id: str, pull_request_id: int, 
                                 project: Optional[str] = None) -> str:
    """
    Get comprehensive details about a specific pull request.
    
    This tool retrieves detailed information about a pull request, including
    description, reviewers, policies, linked work items, and approval status.
    Essential for code review and approval workflows.
    
    Parameters:
        repository_id (str): The repository ID or name.
        pull_request_id (int): The pull request ID number.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: Comprehensive details about the pull request.
    
    Example:
        get_pull_request_details_tool("my-app", 123)
    Output:
        "Pull Request #123: Fix authentication bug
         Status: Active
         Created by: John Doe on 2023-10-01T12:00:00Z
         Source: feature/auth-fix → Target: main
         
         Description:
         This PR fixes the authentication issue where users with special
         characters in passwords couldn't log in.
         
         Reviewers:
         - Jane Smith: Approved [Required]
         - Bob Wilson: Waiting for Author
         
         Linked Work Items:
         - #456: Fix login bug
         
         Merge Status: Succeeded"
    """
    try:
        pr_details = devops.get_pull_request_details(repository_id, pull_request_id, project=project)
        
        if not pr_details:
            return f"Pull request #{pull_request_id} not found in repository '{repository_id}'"
        
        result = f"Pull Request #{pr_details['pullRequestId']}: {pr_details['title']}\n"
        result += f"Status: {pr_details['status'].title()}"
        if pr_details['isDraft']:
            result += " (Draft)"
        result += "\n"
        
        if pr_details['createdBy']:
            result += f"Created by: {pr_details['createdBy']['displayName']}"
            if pr_details['creationDate']:
                result += f" on {pr_details['creationDate']}"
            result += "\n"
        
        if pr_details.get('closedBy') and pr_details.get('closedDate'):
            result += f"Closed by: {pr_details['closedBy']['displayName']} on {pr_details['closedDate']}\n"
        
        # Format branch names
        source_branch = pr_details['sourceRefName'].replace('refs/heads/', '') if pr_details['sourceRefName'] else 'unknown'
        target_branch = pr_details['targetRefName'].replace('refs/heads/', '') if pr_details['targetRefName'] else 'unknown'
        result += f"{source_branch} → {target_branch}\n"
        
        if pr_details['description']:
            result += f"\nDescription:\n{pr_details['description']}\n"
        
        if pr_details['reviewers']:
            result += "\nReviewers:\n"
            for reviewer in pr_details['reviewers']:
                vote_desc = {
                    -10: "Rejected",
                    -5: "Waiting for Author",
                    0: "No Vote", 
                    5: "Approved with Suggestions",
                    10: "Approved"
                }.get(reviewer['vote'], "Unknown")
                
                result += f"- {reviewer['displayName']}: {vote_desc}"
                if reviewer['isRequired']:
                    result += " [Required]"
                if reviewer['isFlagged']:
                    result += " [Flagged]"
                result += "\n"
        
        if pr_details['workItemRefs']:
            result += "\nLinked Work Items:\n"
            for wi in pr_details['workItemRefs']:
                result += f"- #{wi['id']}\n"
        
        if pr_details['labels']:
            result += f"\nLabels: {', '.join(pr_details['labels'])}\n"
        
        if pr_details['mergeStatus']:
            result += f"\nMerge Status: {pr_details['mergeStatus']}\n"
        
        if pr_details['url']:
            result += f"\nURL: {pr_details['url']}\n"
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting pull request details for PR {pull_request_id}: {e}")
        return f"Error getting pull request details for PR {pull_request_id}: {str(e)}"

def create_pull_request_tool(repository_id: str, title: str, description: str,
                            source_branch: str, target_branch: str,
                            reviewers: Optional[List[str]] = None, is_draft: bool = False,
                            project: Optional[str] = None) -> str:
    """
    Create a new pull request in a Git repository.
    
    This tool creates a new pull request with the specified details, reviewers,
    and options. Essential for initiating code review and collaboration workflows.
    
    Parameters:
        repository_id (str): The repository ID or name.
        title (str): The pull request title.
        description (str): The pull request description.
        source_branch (str): The source branch name (without refs/heads/).
        target_branch (str): The target branch name (without refs/heads/).
        reviewers (List[str], optional): List of reviewer IDs, emails, or display names.
        is_draft (bool): Whether to create as a draft PR (default: False).
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: Information about the created pull request.
    
    Example:
        create_pull_request_tool("my-app", "Fix authentication bug", "This PR fixes...", "feature/auth-fix", "main", ["john@example.com"], False)
    Output:
        "Pull request created successfully:
         PR #124: Fix authentication bug
         Status: Active
         Created by: Current User on 2023-10-01T12:00:00Z
         Source: feature/auth-fix → Target: main
         URL: https://dev.azure.com/..."
    """
    try:
        result = devops.create_pull_request(
            repository_id=repository_id,
            title=title,
            description=description,
            source_branch=source_branch,
            target_branch=target_branch,
            reviewers=reviewers,
            is_draft=is_draft,
            project=project
        )
        
        if 'error' in result:
            return f"Error creating pull request: {result['error']}"
        
        response = "Pull request created successfully:\n"
        response += f"PR #{result['pullRequestId']}: {result['title']}\n"
        response += f"Status: {result['status'].title()}"
        if result['isDraft']:
            response += " (Draft)"
        response += "\n"
        
        if result['createdBy']:
            response += f"Created by: {result['createdBy']['displayName']}"
            if result['creationDate']:
                response += f" on {result['creationDate']}"
            response += "\n"
        
        # Format branch names
        source = result['sourceRefName'].replace('refs/heads/', '') if result['sourceRefName'] else source_branch
        target = result['targetRefName'].replace('refs/heads/', '') if result['targetRefName'] else target_branch
        response += f"{source} → {target}\n"
        
        if result['url']:
            response += f"URL: {result['url']}\n"
        
        return response
        
    except Exception as e:
        logging.error(f"Error creating pull request: {e}")
        return f"Error creating pull request: {str(e)}"

def approve_pull_request_tool(repository_id: str, pull_request_id: int, 
                             reviewer_id: str, project: Optional[str] = None) -> str:
    """
    Approve a pull request by casting an approval vote.
    
    This tool allows a reviewer to approve a pull request by casting a vote of 10 (Approved).
    Essential for pull request approval workflows and automated code reviews.
    
    Parameters:
        repository_id (str): The repository ID or name.
        pull_request_id (int): The pull request ID number.
        reviewer_id (str): The reviewer's ID, email, or unique name.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: Confirmation of the approval vote.
    
    Example:
        approve_pull_request_tool("my-app", 123, "john@example.com")
    Output:
        "Pull request approval successful:
         Reviewer: John Doe
         Vote: Approved (10)
         PR #123 in repository my-app"
    """
    try:
        result = devops.update_pull_request_vote(
            repository_id=repository_id,
            pull_request_id=pull_request_id,
            reviewer_id=reviewer_id,
            vote=10,
            project=project
        )
        
        if 'error' in result:
            return f"Error approving pull request: {result['error']}"
        
        response = "Pull request approval successful:\n"
        response += f"Reviewer: {result['displayName']}\n"
        response += f"Vote: {result['voteDescription']} ({result['vote']})\n"
        response += f"PR #{pull_request_id} in repository {repository_id}\n"
        
        if result['isRequired']:
            response += "This was a required reviewer.\n"
        
        return response
        
    except Exception as e:
        logging.error(f"Error approving pull request: {e}")
        return f"Error approving pull request: {str(e)}"

def reject_pull_request_tool(repository_id: str, pull_request_id: int,
                            reviewer_id: str, project: Optional[str] = None) -> str:
    """
    Reject a pull request by casting a rejection vote.
    
    This tool allows a reviewer to reject a pull request by casting a vote of -10 (Rejected).
    Used when changes are required before the PR can be approved.
    
    Parameters:
        repository_id (str): The repository ID or name.
        pull_request_id (int): The pull request ID number.
        reviewer_id (str): The reviewer's ID, email, or unique name.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: Confirmation of the rejection vote.
    
    Example:
        reject_pull_request_tool("my-app", 123, "john@example.com")
    Output:
        "Pull request rejection recorded:
         Reviewer: John Doe
         Vote: Rejected (-10)
         PR #123 in repository my-app"
    """
    try:
        result = devops.update_pull_request_vote(
            repository_id=repository_id,
            pull_request_id=pull_request_id,
            reviewer_id=reviewer_id,
            vote=-10,
            project=project
        )
        
        if 'error' in result:
            return f"Error rejecting pull request: {result['error']}"
        
        response = "Pull request rejection recorded:\n"
        response += f"Reviewer: {result['displayName']}\n"
        response += f"Vote: {result['voteDescription']} ({result['vote']})\n"
        response += f"PR #123 in repository {repository_id}\n"
        
        if result['isRequired']:
            response += "This was a required reviewer.\n"
        
        return response
        
    except Exception as e:
        logging.error(f"Error rejecting pull request: {e}")
        return f"Error rejecting pull request: {str(e)}"

def request_pull_request_changes_tool(repository_id: str, pull_request_id: int,
                                     reviewer_id: str, project: Optional[str] = None) -> str:
    """
    Request changes on a pull request by casting a 'waiting for author' vote.
    
    This tool allows a reviewer to request changes on a pull request by casting
    a vote of -5 (Waiting for Author). Used when minor changes are needed.
    
    Parameters:
        repository_id (str): The repository ID or name.
        pull_request_id (int): The pull request ID number.
        reviewer_id (str): The reviewer's ID, email, or unique name.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: Confirmation of the change request vote.
    
    Example:
        request_pull_request_changes_tool("my-app", 123, "john@example.com")
    Output:
        "Pull request change request recorded:
         Reviewer: John Doe
         Vote: Waiting for Author (-5)
         PR #123 in repository my-app"
    """
    try:
        result = devops.update_pull_request_vote(
            repository_id=repository_id,
            pull_request_id=pull_request_id,
            reviewer_id=reviewer_id,
            vote=-5,
            project=project
        )
        
        if 'error' in result:
            return f"Error requesting changes on pull request: {result['error']}"
        
        response = "Pull request change request recorded:\n"
        response += f"Reviewer: {result['displayName']}\n"
        response += f"Vote: {result['voteDescription']} ({result['vote']})\n"
        response += f"PR #123 in repository {repository_id}\n"
        
        if result['isRequired']:
            response += "This was a required reviewer.\n"
        
        return response
        
    except Exception as e:
        logging.error(f"Error requesting changes on pull request: {e}")
        return f"Error requesting changes on pull request: {str(e)}"

def get_pull_request_policies_tool(repository_id: str, pull_request_id: int,
                                  project: Optional[str] = None) -> str:
    """
    Get branch policies and their status for a pull request.
    
    This tool retrieves information about branch policies that apply to a pull request,
    including their evaluation status. Essential for understanding approval requirements
    and compliance checks.
    
    Parameters:
        repository_id (str): The repository ID or name.
        pull_request_id (int): The pull request ID number.
        project (str, optional): The Azure DevOps project name. If not provided, uses the default project.
    
    Returns:
        str: Information about branch policies and their evaluation status.
    
    Example:
        get_pull_request_policies_tool("my-app", 123)
    Output:
        "Branch policies for PR #123:
        
        Policy: Minimum number of reviewers
        Status: Approved
        Started: 2023-10-01T12:00:00Z
        Completed: 2023-10-01T12:30:00Z
        
        Policy: Build validation
        Status: Running
        Started: 2023-10-01T12:00:00Z"
    """
    try:
        policies = devops.get_pull_request_policies(repository_id, pull_request_id, project=project)
        
        if not policies:
            return f"No branch policies found for PR #{pull_request_id} in repository '{repository_id}'"
        
        result = f"Branch policies for PR #{pull_request_id}:\n\n"
        
        for policy in policies:
            # Extract policy name from configuration if available
            policy_name = "Unknown Policy"
            if policy.get('configuration') and isinstance(policy['configuration'], dict):
                config = policy['configuration']
                if 'displayName' in config:
                    policy_name = config['displayName']
                elif 'type' in config:
                    policy_name = config['type']['displayName'] if isinstance(config['type'], dict) else str(config['type'])
            
            result += f"Policy: {policy_name}\n"
            result += f"Status: {policy['status']}\n"
            result += f"Evaluation ID: {policy['evaluationId']}\n"
            
            if policy['startedDate']:
                result += f"Started: {policy['startedDate']}\n"
            if policy['completedDate']:
                result += f"Completed: {policy['completedDate']}\n"
            
            result += "\n"
        
        return result.rstrip()
        
    except Exception as e:
        logging.error(f"Error getting policies for PR {pull_request_id}: {e}")
        return f"Error getting policies for PR {pull_request_id}: {str(e)}"


# Export all tools for easy MCP integration
__all__ = [
    # Core tool functions
    "get_changeset_tool",
    "get_file_diff_tool", 
    "get_changeset_changes_tool",
    "get_changeset_list_tool",
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
    "get_projects_tool",
]
