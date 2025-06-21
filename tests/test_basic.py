"""
Basic tests for azuredevops-tools package.
"""

import pytest
from azuredevops_tools import __version__


def test_version():
    """Test that version is defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_package_import():
    """Test that main package can be imported."""
    import azuredevops_tools
    assert azuredevops_tools is not None


def test_tools_import():
    """Test that tools module can be imported."""
    try:
        from azuredevops_tools import tools
        assert tools is not None
    except ImportError:
        # Skip if tools require Azure DevOps credentials
        pytest.skip("Tools module requires Azure DevOps credentials")
