# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-09-21

### Added
- Comprehensive Git tools for Azure DevOps integration:
  - Git repository management tools (`get_git_repositories_tool`, `get_git_repository_tool`)
  - Git commit analysis tools (`get_git_commits_tool`, `get_git_commit_details_tool`)
  - Pull request workflow tools (`get_pull_requests_tool`, `get_pull_request_details_tool`)
  - Pull request actions (`create_pull_request_tool`, `approve_pull_request_tool`, `reject_pull_request_tool`, `request_pull_request_changes_tool`)
  - Pull request policy validation (`get_pull_request_policies_tool`)
- Project management tools (`get_projects_tool`) for Azure DevOps organization discovery
- Enhanced Git commits retrieval with improved error handling and LLM-friendly formatting
- Search criteria functionality for improved Git commit filtering
- Docker containerization support with optimized Dockerfile and .dockerignore
- Comprehensive MCP server integration with 22 registered tools
- Extensive documentation including:
  - Git tools implementation summary
  - MCP server integration guide
  - Tools registration summary
- Complete test suite for Git tools and MCP server functionality
- Example scripts demonstrating Git operations and workflows

### Changed
- Enhanced error handling across all Git-related operations
- Improved formatting of Git commit information for better LLM integration
- Updated MCP server configuration with proper environment variable setup
- Expanded tool registration to include all Git and project management tools

### Fixed
- Codecov condition and file parameter corrections in CI workflow
- Docker container shebang handling for virtual environment executables

### Dependencies
- Updated python-dotenv from 1.1.0 to 1.1.1
- Updated pytest from 8.4.1 to 8.4.2
- Updated pytest-cov from 6.2.1 to 7.0.0
- Updated GitHub Actions dependencies:
  - actions/checkout from v4 to v5
  - actions/setup-python from v5 to v6
  - actions/download-artifact from v4 to v5

### Documentation
- Added comprehensive documentation for Git tools implementation
- Created MCP server integration guide
- Added tools registration summary with categorized tool listings
- Updated README with new Git tools capabilities

## [0.1.1] - 2025-06-21

### Changed
- Updated Dependabot configuration to use "uv" package ecosystem instead of "pip"
- Upgraded GitHub Actions dependencies:
  - actions/setup-python from v4 to v5
  - codecov/codecov-action from v3 to v5
  - astral-sh/setup-uv from v2 to v6
  - actions/upload-artifact and actions/download-artifact to v4

### Added
- GitHub Actions CI/CD workflows for automated testing and PyPI publishing
- Comprehensive test suite with pytest
- Development Makefile for common tasks
- Code quality checks with black, isort, and flake8

### Changed
- Updated README with CI/CD and publishing information
- Improved package structure and development setup

## [0.1.0] - 2025-06-21

### Added
- Initial release of Azure DevOps Tools for MCP integration
- Changeset analysis tools (get_changeset_tool, get_file_diff_tool, etc.)
- Build monitoring tools (get_build_tool, get_builds_tool, etc.)
- Pipeline management tools (get_build_pipelines_tool)
- Diagnostic tools (get_failed_tasks_with_logs_tool)
- Multi-project support with optional project parameter
- MCP server implementation for LLM integration
- Comprehensive documentation and examples
- MIT License

### Security
- Environment-based credential management with .env support
- Trusted publishing setup for secure PyPI deployment
