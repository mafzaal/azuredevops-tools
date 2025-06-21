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
]
