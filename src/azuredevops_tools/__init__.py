"""
Azure DevOps Tools Package

A comprehensive package for interacting with Azure DevOps through the Model Context Protocol (MCP).
Provides tools for changesets, builds, pipelines, and code analysis.
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
)
from .main import main

__version__ = "0.1.1"
__all__ = [
    "DevOpsToolset",
    "main",
    "get_changeset_tool",
    "get_changeset_changes_tool", 
    "get_changeset_list_tool",
    "get_file_diff_tool",
    "get_build_tool",
    "get_builds_tool",
    "get_build_logs_tool",
    "get_build_log_full_content_tool",
    "get_failed_tasks_with_logs_tool",
    "get_build_pipelines_tool",
]
