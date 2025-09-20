---
mode: agent
description: Update the change log file with the latest changes based on recent commits and increment version numbers.
---

# AI Assistant Instructions: Update Changelog and Version Numbers

## Overview
These instructions guide an AI assistant to systematically update the project's CHANGELOG.md and increment version numbers in pyproject.toml and __init__.py based on git commit history.

## Process Steps

### 1. Examine Current Version Files
- Read `pyproject.toml` to identify current version number
- Read `src/azuredevops_tools/__init__.py` to verify version consistency
- Read `CHANGELOG.md` to understand the last documented version and changes

### 2. Analyze Git History
- Use `git log --oneline --since="YYYY-MM-DD" --pretty=format:"%h %s" --reverse` to get commits since last changelog entry
- Use `git log --since="YYYY-MM-DD" --pretty=format:"%h %s%n%b" --reverse` for detailed commit messages
- Use `git show --stat <commit-hashes> --pretty=format:"%h %s"` to understand scope of changes

### 3. Determine Version Increment Strategy
Follow semantic versioning (semver.org):
- **MAJOR (X.0.0)**: Breaking changes, incompatible API changes
- **MINOR (0.X.0)**: New features, backward-compatible functionality additions
- **PATCH (0.0.X)**: Bug fixes, backward-compatible fixes

Common indicators:
- New tools/features → MINOR bump
- Bug fixes only → PATCH bump
- Breaking API changes → MAJOR bump
- Dependency updates alone → PATCH bump

### 4. Update CHANGELOG.md
Follow "Keep a Changelog" format:
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features, tools, capabilities

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes and corrections

### Dependencies
- Dependency updates

### Documentation
- Documentation improvements
```

Categories to look for in commits:
- `feat:` → Added section
- `fix:` → Fixed section
- `deps:` or `Bump` → Dependencies section
- `docs:` → Documentation section
- `ci:` → Usually Dependencies section
- `chore:` → May go in Changed or omit if minor

### 5. Update Version Numbers
Update in exact order:
1. **pyproject.toml**: Change version = "X.Y.Z"
2. **__init__.py**: Change __version__ = "X.Y.Z"

### 6. Quality Checks
- Ensure version numbers match across all files
- Verify changelog entry has proper date format (YYYY-MM-DD)
- Check that changes are categorized appropriately
- Confirm semantic versioning logic is sound

## File Locations
- **Version source**: `pyproject.toml` (line ~7)
- **Version sync**: `src/azuredevops_tools/__init__.py` (line ~33)
- **Changelog**: `CHANGELOG.md` (top of file)

## Git Commands Reference
```bash
# Get commits since last release
git log --oneline --since="2025-06-21" --pretty=format:"%h %s" --reverse

# Get detailed commit info
git log --since="2025-06-21" --pretty=format:"%h %s%n%b" --reverse

# Show file changes for specific commits
git show --stat <commit1> <commit2> --pretty=format:"%h %s"
```

## Example Workflow
1. Read current version (e.g., 0.2.0)
2. Analyze commits → Major Git tools added + new features
3. Determine: MINOR bump → 0.3.0
4. Update CHANGELOG.md with new 0.3.0 section
5. Update pyproject.toml version to 0.3.0
6. Update __init__.py __version__ to 0.3.0

## Common Pitfalls to Avoid
- Don't mix up version numbers between files
- Don't skip dependency updates in changelog
- Don't use wrong date format
- Don't forget to categorize changes properly
- Don't increment version incorrectly for scope of changes

## Success Criteria
✅ CHANGELOG.md has new version entry with proper date
✅ All changes from git history are documented appropriately
✅ Version numbers match in pyproject.toml and __init__.py
✅ Semantic versioning logic is correctly applied
✅ Changelog follows "Keep a Changelog" format
