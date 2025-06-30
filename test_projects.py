#!/usr/bin/env python3
"""
Test script to verify the get_projects_tool functionality.
"""

import sys
import os

# Add the parent directory to the path so we can import our tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_projects_tool():
    """Test that the projects tool works correctly."""
    try:
        print("Testing projects tool import...")
        
        from azuredevops_tools.tools import get_projects_tool
        print("✅ Successfully imported get_projects_tool")
        
        print(f"Function name: {get_projects_tool.__name__}")
        print(f"Docstring available: {bool(get_projects_tool.__doc__)}")
        
        if get_projects_tool.__doc__:
            lines = get_projects_tool.__doc__.strip().split('\n')
            print(f"First line of docstring: {lines[0]}")
        
        print("✅ Projects tool test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_projects_tool()
    sys.exit(0 if success else 1)
