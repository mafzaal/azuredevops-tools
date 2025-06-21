# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
