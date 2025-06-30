#!/usr/bin/env python3
"""
Git Tools Examples for Azure DevOps Integration

This script demonstrates how to use the Git-related tools for Azure DevOps,
including repository management, commit analysis, pull request workflows,
and approval processes.

Before running this script, ensure you have set up the required environment variables:
- DEVOPS_PAT: Your Azure DevOps Personal Access Token
- DEVOPS_ORGANIZATION: Your Azure DevOps organization name
- DEVOPS_PROJECT: Your Azure DevOps project name
"""

import sys
import os

# Add the parent directory to the path so we can import our tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from azuredevops_tools.tools import (
    get_git_repositories_tool,
    get_git_repository_tool,
    get_git_commits_tool,
    get_git_commit_details_tool,
    get_pull_requests_tool,
    get_pull_request_details_tool,
    create_pull_request_tool,
    approve_pull_request_tool,
    reject_pull_request_tool,
    request_pull_request_changes_tool,
    get_pull_request_policies_tool
)


def demonstrate_git_repositories():
    """Demonstrate Git repository discovery and information retrieval."""
    print("=" * 80)
    print("GIT REPOSITORY OPERATIONS")
    print("=" * 80)
    
    # Get all repositories in the project
    print("\n1. Getting all Git repositories in the project:")
    print("-" * 50)
    repositories = get_git_repositories_tool()
    print(repositories)
    
    # Get details for a specific repository (replace with your repo name)
    repo_name = "your-repo-name"  # Replace with actual repository name
    print(f"\n2. Getting details for repository '{repo_name}':")
    print("-" * 50)
    repo_details = get_git_repository_tool(repo_name)
    print(repo_details)


def demonstrate_git_commits():
    """Demonstrate Git commit analysis and history retrieval."""
    print("\n" + "=" * 80)
    print("GIT COMMIT OPERATIONS")
    print("=" * 80)
    
    repo_name = "your-repo-name"  # Replace with actual repository name
    
    # Get recent commits from main branch
    print(f"\n3. Getting recent commits from repository '{repo_name}':")
    print("-" * 50)
    commits = get_git_commits_tool(repo_name, branch="main", top=5)
    print(commits)
    
    # Get detailed information about a specific commit (replace with actual commit ID)
    commit_id = "abc123def456"  # Replace with actual commit SHA
    print(f"\n4. Getting details for commit '{commit_id}':")
    print("-" * 50)
    commit_details = get_git_commit_details_tool(repo_name, commit_id)
    print(commit_details)


def demonstrate_pull_requests():
    """Demonstrate pull request management and workflows."""
    print("\n" + "=" * 80)
    print("PULL REQUEST OPERATIONS")
    print("=" * 80)
    
    repo_name = "your-repo-name"  # Replace with actual repository name
    
    # Get active pull requests
    print(f"\n5. Getting active pull requests from repository '{repo_name}':")
    print("-" * 50)
    active_prs = get_pull_requests_tool(repo_name, status="active", top=10)
    print(active_prs)
    
    # Get all pull requests (active, completed, abandoned)
    print(f"\n6. Getting all pull requests from repository '{repo_name}':")
    print("-" * 50)
    all_prs = get_pull_requests_tool(repo_name, status="all", top=20)
    print(all_prs)
    
    # Get pull requests targeting main branch
    print(f"\n7. Getting pull requests targeting 'main' branch:")
    print("-" * 50)
    main_prs = get_pull_requests_tool(repo_name, status="active", target_branch="main")
    print(main_prs)


def demonstrate_pull_request_details():
    """Demonstrate detailed pull request analysis."""
    print("\n" + "=" * 80)
    print("PULL REQUEST DETAILS")
    print("=" * 80)
    
    repo_name = "your-repo-name"  # Replace with actual repository name
    pr_id = 123  # Replace with actual PR ID
    
    # Get detailed information about a specific pull request
    print(f"\n8. Getting details for pull request #{pr_id}:")
    print("-" * 50)
    pr_details = get_pull_request_details_tool(repo_name, pr_id)
    print(pr_details)
    
    # Get branch policies for the pull request
    print(f"\n9. Getting branch policies for pull request #{pr_id}:")
    print("-" * 50)
    pr_policies = get_pull_request_policies_tool(repo_name, pr_id)
    print(pr_policies)


def demonstrate_pull_request_creation():
    """Demonstrate pull request creation workflow."""
    print("\n" + "=" * 80)
    print("PULL REQUEST CREATION")
    print("=" * 80)
    
    repo_name = "your-repo-name"  # Replace with actual repository name
    
    # Create a new pull request
    print(f"\n10. Creating a new pull request in repository '{repo_name}':")
    print("-" * 50)
    
    # Example PR creation (uncomment and modify for actual use)
    """
    new_pr = create_pull_request_tool(
        repository_id=repo_name,
        title="Fix authentication bug",
        description="This PR fixes the authentication issue where users with special characters in passwords couldn't log in.\n\nChanges:\n- Updated password validation logic\n- Added unit tests for special character handling\n- Updated documentation",
        source_branch="feature/auth-fix",
        target_branch="main",
        reviewers=["reviewer1@company.com", "reviewer2@company.com"],
        is_draft=False
    )
    print(new_pr)
    """
    print("PR creation example (commented out - modify with real values)")


def demonstrate_pull_request_approvals():
    """Demonstrate pull request approval workflows."""
    print("\n" + "=" * 80)
    print("PULL REQUEST APPROVAL WORKFLOWS")
    print("=" * 80)
    
    repo_name = "your-repo-name"  # Replace with actual repository name
    pr_id = 123  # Replace with actual PR ID
    reviewer_id = "reviewer@company.com"  # Replace with actual reviewer
    
    print(f"\n11. Pull request approval operations for PR #{pr_id}:")
    print("-" * 50)
    
    # Example approval operations (uncomment and modify for actual use)
    """
    # Approve a pull request
    approval = approve_pull_request_tool(repo_name, pr_id, reviewer_id)
    print("Approval result:")
    print(approval)
    print()
    
    # Request changes on a pull request
    changes = request_pull_request_changes_tool(repo_name, pr_id, reviewer_id)
    print("Change request result:")
    print(changes)
    print()
    
    # Reject a pull request
    rejection = reject_pull_request_tool(repo_name, pr_id, reviewer_id)
    print("Rejection result:")
    print(rejection)
    """
    print("Approval workflow examples (commented out - modify with real values)")


def demonstrate_workflow_scenarios():
    """Demonstrate common Git workflow scenarios."""
    print("\n" + "=" * 80)
    print("COMMON WORKFLOW SCENARIOS")
    print("=" * 80)
    
    repo_name = "your-repo-name"  # Replace with actual repository name
    
    print("\n12. Scenario: Code Review Workflow")
    print("-" * 50)
    print("1. Developer creates feature branch and commits changes")
    print("2. Developer creates pull request:")
    print(f"   create_pull_request_tool('{repo_name}', 'Feature: Add login', 'Description...', 'feature/login', 'main')")
    print("3. Reviewers examine the PR:")
    print(f"   get_pull_request_details_tool('{repo_name}', pr_id)")
    print("4. Reviewers approve or request changes:")
    print(f"   approve_pull_request_tool('{repo_name}', pr_id, reviewer_id)")
    print("5. Check if all policies are satisfied:")
    print(f"   get_pull_request_policies_tool('{repo_name}', pr_id)")
    
    print("\n13. Scenario: Release Management")
    print("-" * 50)
    print("1. Get commits since last release:")
    print(f"   get_git_commits_tool('{repo_name}', 'main', top=50)")
    print("2. Analyze commit details for release notes:")
    print(f"   get_git_commit_details_tool('{repo_name}', commit_id)")
    print("3. Create release PR:")
    print(f"   create_pull_request_tool('{repo_name}', 'Release v1.2.0', 'Description...', 'release/v1.2.0', 'main')")
    
    print("\n14. Scenario: Repository Audit")
    print("-" * 50)
    print("1. Get all repositories in the project:")
    print("   get_git_repositories_tool()")
    print("2. For each repository, check recent activity:")
    print(f"   get_git_commits_tool(repo_name, top=10)")
    print("3. Check open pull requests:")
    print(f"   get_pull_requests_tool(repo_name, 'active')")
    print("4. Review stale pull requests:")
    print(f"   get_pull_requests_tool(repo_name, 'all')")


def main():
    """Main function to run all demonstrations."""
    print("Azure DevOps Git Tools Demonstration")
    print("=" * 80)
    print("This script demonstrates the Git-related tools for Azure DevOps integration.")
    print("Replace placeholder values (repository names, PR IDs, etc.) with real values.")
    print("Uncomment the actual API calls when ready to test with real data.")
    
    try:
        # Repository operations
        demonstrate_git_repositories()
        
        # Commit operations
        demonstrate_git_commits()
        
        # Pull request operations
        demonstrate_pull_requests()
        demonstrate_pull_request_details()
        
        # PR creation and approval workflows
        demonstrate_pull_request_creation()
        demonstrate_pull_request_approvals()
        
        # Common workflow scenarios
        demonstrate_workflow_scenarios()
        
        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETE")
        print("=" * 80)
        print("To use these tools with real data:")
        print("1. Set up your environment variables (DEVOPS_PAT, DEVOPS_ORGANIZATION, DEVOPS_PROJECT)")
        print("2. Replace placeholder values with real repository names, PR IDs, etc.")
        print("3. Uncomment the actual API calls")
        print("4. Run the script to interact with your Azure DevOps project")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        print("Make sure your Azure DevOps credentials are configured correctly.")


if __name__ == "__main__":
    main()
