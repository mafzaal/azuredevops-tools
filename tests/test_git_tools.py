#!/usr/bin/env python3
"""
Test suite for Git tools in Azure DevOps integration.

This test file validates the Git-related functionality including:
- Repository discovery and management
- Commit analysis and history
- Pull request workflows
- Approval processes
- Policy compliance checking

Run with: python -m pytest tests/test_git_tools.py -v
"""

import pytest
import unittest.mock as mock
from typing import Dict, Any, List

# Import the tools to test
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


# Mock data for testing
MOCK_REPOSITORY = {
    'id': 'abc123-def456-ghi789',
    'name': 'test-repo',
    'url': 'https://dev.azure.com/org/project/_apis/git/repositories/test-repo',
    'defaultBranch': 'refs/heads/main',
    'size': 15728640,  # 15 MB
    'remoteUrl': 'https://dev.azure.com/org/project/_git/test-repo',
    'sshUrl': 'git@ssh.dev.azure.com:v3/org/project/test-repo',
    'webUrl': 'https://dev.azure.com/org/project/_git/test-repo',
    'isDisabled': False,
    'isFork': False,
    'projectId': 'project123',
    'projectName': 'TestProject'
}

MOCK_COMMIT = {
    'commitId': 'abc123def456789',
    'comment': 'Fix authentication bug',
    'author': {
        'name': 'John Doe',
        'email': 'john@example.com',
        'date': '2023-10-01T12:00:00Z'
    },
    'committer': {
        'name': 'John Doe',
        'email': 'john@example.com',
        'date': '2023-10-01T12:00:00Z'
    },
    'changeCounts': {'Add': 5, 'Edit': 3, 'Delete': 1},
    'url': 'https://dev.azure.com/org/project/_git/test-repo/commit/abc123def456789',
    'remoteUrl': 'https://dev.azure.com/org/project/_git/test-repo/commit/abc123def456789'
}

MOCK_PULL_REQUEST = {
    'pullRequestId': 123,
    'title': 'Fix authentication bug',
    'description': 'This PR fixes the authentication issue...',
    'status': 'active',
    'createdBy': {
        'displayName': 'John Doe',
        'uniqueName': 'john@example.com',
        'id': 'user123'
    },
    'creationDate': '2023-10-01T12:00:00Z',
    'closedDate': None,
    'sourceRefName': 'refs/heads/feature/auth-fix',
    'targetRefName': 'refs/heads/main',
    'lastMergeSourceCommit': 'abc123def456',
    'lastMergeTargetCommit': 'def456ghi789',
    'isDraft': False,
    'mergeStatus': 'succeeded',
    'url': 'https://dev.azure.com/org/project/_git/test-repo/pullrequest/123',
    'reviewers': [
        {
            'displayName': 'Jane Smith',
            'uniqueName': 'jane@example.com',
            'id': 'reviewer1',
            'vote': 10,  # Approved
            'isRequired': True,
            'isFlagged': False
        }
    ]
}


class TestGitRepositoryTools:
    """Test Git repository management tools."""
    
    @mock.patch('azuredevops_tools.tools.devops.get_git_repositories')
    def test_get_git_repositories_tool_success(self, mock_get_repos):
        """Test successful repository listing."""
        mock_get_repos.return_value = [MOCK_REPOSITORY]
        
        result = get_git_repositories_tool()
        
        assert "Found 1 Git repositories" in result
        assert "test-repo" in result
        assert "15.0 MB" in result
        assert "Active" in result
        mock_get_repos.assert_called_once_with(project=None)
    
    @mock.patch('azuredevops_tools.tools.devops.get_git_repositories')
    def test_get_git_repositories_tool_empty(self, mock_get_repos):
        """Test repository listing with no repositories."""
        mock_get_repos.return_value = []
        
        result = get_git_repositories_tool()
        
        assert "No Git repositories found" in result
    
    @mock.patch('azuredevops_tools.tools.devops.get_git_repository')
    def test_get_git_repository_tool_success(self, mock_get_repo):
        """Test successful single repository retrieval."""
        mock_get_repo.return_value = MOCK_REPOSITORY
        
        result = get_git_repository_tool("test-repo")
        
        assert "Repository: test-repo" in result
        assert "refs/heads/main" in result
        assert "Active" in result
        mock_get_repo.assert_called_once_with("test-repo", project=None)
    
    @mock.patch('azuredevops_tools.tools.devops.get_git_repository')
    def test_get_git_repository_tool_not_found(self, mock_get_repo):
        """Test repository retrieval for non-existent repository."""
        mock_get_repo.return_value = {}
        
        result = get_git_repository_tool("invalid-repo")
        
        assert "not found" in result


class TestGitCommitTools:
    """Test Git commit analysis tools."""
    
    @mock.patch('azuredevops_tools.tools.devops.get_git_commits')
    def test_get_git_commits_tool_success(self, mock_get_commits):
        """Test successful commit listing."""
        mock_get_commits.return_value = [MOCK_COMMIT]
        
        result = get_git_commits_tool("test-repo", "main", 5)
        
        assert "Found 1 commits from repository test-repo" in result
        assert "abc123def456" in result
        assert "John Doe" in result
        assert "Fix authentication bug" in result
        assert "+5 ~3 -1" in result
        mock_get_commits.assert_called_once_with("test-repo", branch="main", top=5, project=None)
    
    @mock.patch('azuredevops_tools.tools.devops.get_git_commits')
    def test_get_git_commits_tool_empty(self, mock_get_commits):
        """Test commit listing with no commits."""
        mock_get_commits.return_value = []
        
        result = get_git_commits_tool("test-repo")
        
        assert "No commits found" in result
    
    @mock.patch('azuredevops_tools.tools.devops.get_git_commit_details')
    def test_get_git_commit_details_tool_success(self, mock_get_details):
        """Test successful commit details retrieval."""
        commit_details = MOCK_COMMIT.copy()
        commit_details['changes'] = [
            {
                'changeType': 'Edit',
                'item': {'path': 'src/auth.py', 'gitObjectType': 'blob'}
            }
        ]
        mock_get_details.return_value = commit_details
        
        result = get_git_commit_details_tool("test-repo", "abc123")
        
        assert "Commit: abc123def456789" in result
        assert "John Doe <john@example.com>" in result
        assert "Fix authentication bug" in result
        assert "src/auth.py (Edit)" in result
        mock_get_details.assert_called_once_with("test-repo", "abc123", project=None)


class TestPullRequestTools:
    """Test pull request management tools."""
    
    @mock.patch('azuredevops_tools.tools.devops.get_pull_requests')
    def test_get_pull_requests_tool_success(self, mock_get_prs):
        """Test successful pull request listing."""
        mock_get_prs.return_value = [MOCK_PULL_REQUEST]
        
        result = get_pull_requests_tool("test-repo", "active")
        
        assert "Found 1 active in repository test-repo" in result
        assert "PR #123: Fix authentication bug" in result
        assert "John Doe" in result
        assert "feature/auth-fix → main" in result
        assert "Jane Smith (Approved)" in result
        mock_get_prs.assert_called_once()
    
    @mock.patch('azuredevops_tools.tools.devops.get_pull_requests')
    def test_get_pull_requests_tool_with_filters(self, mock_get_prs):
        """Test pull request listing with filters."""
        mock_get_prs.return_value = [MOCK_PULL_REQUEST]
        
        result = get_pull_requests_tool("test-repo", "active", target_branch="main")
        
        mock_get_prs.assert_called_once_with(
            repository_id="test-repo",
            status="active",
            target_branch="main",
            source_branch=None,
            top=20,
            project=None
        )
    
    @mock.patch('azuredevops_tools.tools.devops.get_pull_request_details')
    def test_get_pull_request_details_tool_success(self, mock_get_details):
        """Test successful pull request details retrieval."""
        pr_details = MOCK_PULL_REQUEST.copy()
        pr_details['workItemRefs'] = [{'id': 456, 'url': 'https://...'}]
        pr_details['labels'] = ['bug', 'security']
        mock_get_details.return_value = pr_details
        
        result = get_pull_request_details_tool("test-repo", 123)
        
        assert "Pull Request #123: Fix authentication bug" in result
        assert "Status: Active" in result
        assert "feature/auth-fix → main" in result
        assert "Jane Smith: Approved [Required]" in result
        assert "#456" in result
        assert "bug, security" in result
        mock_get_details.assert_called_once_with("test-repo", 123, project=None)


class TestPullRequestCreation:
    """Test pull request creation tools."""
    
    @mock.patch('azuredevops_tools.tools.devops.create_pull_request')
    def test_create_pull_request_tool_success(self, mock_create):
        """Test successful pull request creation."""
        created_pr = {
            'pullRequestId': 124,
            'title': 'New Feature',
            'description': 'Description...',
            'status': 'active',
            'createdBy': {'displayName': 'John Doe'},
            'creationDate': '2023-10-01T12:00:00Z',
            'sourceRefName': 'refs/heads/feature/new',
            'targetRefName': 'refs/heads/main',
            'isDraft': False,
            'url': 'https://...'
        }
        mock_create.return_value = created_pr
        
        result = create_pull_request_tool(
            "test-repo", "New Feature", "Description...",
            "feature/new", "main", ["reviewer@example.com"]
        )
        
        assert "Pull request created successfully" in result
        assert "PR #124: New Feature" in result
        assert "feature/new → main" in result
        mock_create.assert_called_once()
    
    @mock.patch('azuredevops_tools.tools.devops.create_pull_request')
    def test_create_pull_request_tool_error(self, mock_create):
        """Test pull request creation error handling."""
        mock_create.return_value = {'error': 'Permission denied'}
        
        result = create_pull_request_tool(
            "test-repo", "New Feature", "Description...",
            "feature/new", "main"
        )
        
        assert "Error creating pull request: Permission denied" in result


class TestPullRequestApproval:
    """Test pull request approval workflow tools."""
    
    @mock.patch('azuredevops_tools.tools.devops.update_pull_request_vote')
    def test_approve_pull_request_tool_success(self, mock_vote):
        """Test successful pull request approval."""
        mock_vote.return_value = {
            'reviewerId': 'user123',
            'displayName': 'John Doe',
            'vote': 10,
            'voteDescription': 'Approved',
            'isRequired': True,
            'isFlagged': False
        }
        
        result = approve_pull_request_tool("test-repo", 123, "john@example.com")
        
        assert "Pull request approval successful" in result
        assert "John Doe" in result
        assert "Approved (10)" in result
        assert "required reviewer" in result
        mock_vote.assert_called_once_with(
            repository_id="test-repo",
            pull_request_id=123,
            reviewer_id="john@example.com",
            vote=10,
            project=None
        )
    
    @mock.patch('azuredevops_tools.tools.devops.update_pull_request_vote')
    def test_reject_pull_request_tool_success(self, mock_vote):
        """Test successful pull request rejection."""
        mock_vote.return_value = {
            'reviewerId': 'user123',
            'displayName': 'John Doe',
            'vote': -10,
            'voteDescription': 'Rejected',
            'isRequired': False,
            'isFlagged': False
        }
        
        result = reject_pull_request_tool("test-repo", 123, "john@example.com")
        
        assert "Pull request rejection recorded" in result
        assert "Rejected (-10)" in result
        mock_vote.assert_called_once_with(
            repository_id="test-repo",
            pull_request_id=123,
            reviewer_id="john@example.com",
            vote=-10,
            project=None
        )
    
    @mock.patch('azuredevops_tools.tools.devops.update_pull_request_vote')
    def test_request_pull_request_changes_tool_success(self, mock_vote):
        """Test successful pull request change request."""
        mock_vote.return_value = {
            'reviewerId': 'user123',
            'displayName': 'John Doe',
            'vote': -5,
            'voteDescription': 'Waiting for Author',
            'isRequired': False,
            'isFlagged': False
        }
        
        result = request_pull_request_changes_tool("test-repo", 123, "john@example.com")
        
        assert "Pull request change request recorded" in result
        assert "Waiting for Author (-5)" in result
        mock_vote.assert_called_once_with(
            repository_id="test-repo",
            pull_request_id=123,
            reviewer_id="john@example.com",
            vote=-5,
            project=None
        )


class TestPullRequestPolicies:
    """Test pull request policy tools."""
    
    @mock.patch('azuredevops_tools.tools.devops.get_pull_request_policies')
    def test_get_pull_request_policies_tool_success(self, mock_get_policies):
        """Test successful policy retrieval."""
        mock_policies = [
            {
                'evaluationId': 'eval123',
                'status': 'Approved',
                'policyId': 'policy123',
                'startedDate': '2023-10-01T12:00:00Z',
                'completedDate': '2023-10-01T12:30:00Z',
                'context': {},
                'configuration': {
                    'displayName': 'Minimum number of reviewers',
                    'type': {'displayName': 'Reviewer Policy'}
                }
            }
        ]
        mock_get_policies.return_value = mock_policies
        
        result = get_pull_request_policies_tool("test-repo", 123)
        
        assert "Branch policies for PR #123" in result
        assert "Minimum number of reviewers" in result
        assert "Status: Approved" in result
        assert "eval123" in result
        mock_get_policies.assert_called_once_with("test-repo", 123, project=None)
    
    @mock.patch('azuredevops_tools.tools.devops.get_pull_request_policies')
    def test_get_pull_request_policies_tool_empty(self, mock_get_policies):
        """Test policy retrieval with no policies."""
        mock_get_policies.return_value = []
        
        result = get_pull_request_policies_tool("test-repo", 123)
        
        assert "No branch policies found" in result


class TestErrorHandling:
    """Test error handling across all Git tools."""
    
    @mock.patch('azuredevops_tools.tools.devops.get_git_repositories')
    def test_git_repositories_error_handling(self, mock_get_repos):
        """Test error handling in repository listing."""
        mock_get_repos.side_effect = Exception("Network error")
        
        result = get_git_repositories_tool()
        
        assert "Error getting Git repositories: Network error" in result
    
    @mock.patch('azuredevops_tools.tools.devops.get_pull_requests')
    def test_pull_requests_error_handling(self, mock_get_prs):
        """Test error handling in pull request listing."""
        mock_get_prs.side_effect = Exception("Permission denied")
        
        result = get_pull_requests_tool("test-repo")
        
        assert "Error getting pull requests from test-repo: Permission denied" in result
    
    @mock.patch('azuredevops_tools.tools.devops.update_pull_request_vote')
    def test_approval_error_handling(self, mock_vote):
        """Test error handling in approval workflow."""
        mock_vote.return_value = {'error': 'Invalid reviewer'}
        
        result = approve_pull_request_tool("test-repo", 123, "invalid@example.com")
        
        assert "Error approving pull request: Invalid reviewer" in result


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
