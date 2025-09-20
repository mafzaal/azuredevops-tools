"""
Azure DevOps Tools Package

A comprehensive package for interacting with Azure DevOps through the Model Context Protocol (MCP).
Provides tools for changesets, builds, pipelines, Git repositories, pull requests, and approval workflows.
"""

from .devops_tools import DevOpsToolset
from .tools import (
    get_changeset_tool,
    get_changeset_changes_tool, 
    get_changeset_list_tool,
    get_file_diff_tool,
    get_build_tool,
    get_builds_tool,
    get_build_logs_tool,
    get_build_log_full_content_tool,
    get_failed_tasks_with_logs_tool,
    get_build_pipelines_tool,
    # Git repository tools
    get_git_repositories_tool,
    get_git_repository_tool,
    get_git_commits_tool,
    get_git_commit_details_tool,
    # Pull request tools
    get_pull_requests_tool,
    get_pull_request_details_tool,
    create_pull_request_tool,
    approve_pull_request_tool,
    reject_pull_request_tool,
    request_pull_request_changes_tool,
    get_pull_request_policies_tool,
)
from .main import main

__version__ = "0.3.0"
__all__ = [
    "DevOpsToolset",
    "main",
    # Core changeset tools
    "get_changeset_tool",
    "get_changeset_changes_tool", 
    "get_changeset_list_tool",
    "get_file_diff_tool",
    # Build and pipeline tools
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
