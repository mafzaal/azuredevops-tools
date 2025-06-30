#!/usr/bin/env python3
"""
Simple test to check if FastMCP tool registration works.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def simple_test_tool(name: str) -> str:
    """A simple test tool."""
    return f"Hello from {name}!"

def test_fastmcp():
    """Test FastMCP tool registration."""
    try:
        from mcp.server.fastmcp import FastMCP
        
        print("Testing FastMCP...")
        server = FastMCP("test_server")
        print(f"✅ FastMCP server created: {server.name}")
        
        # Add a simple test tool
        server.add_tool(simple_test_tool)
        print("✅ Test tool added successfully")
        
        # Try to inspect the server
        print(f"Server type: {type(server)}")
        
        # Try to find registered tools
        if hasattr(server, 'tools'):
            print(f"Found tools attribute: {len(server.tools)} tools")
        else:
            print("No tools attribute found")
            
        if hasattr(server, '_tools'):
            print(f"Found _tools attribute: {len(server._tools)} tools")
        else:
            print("No _tools attribute found")
            
        # Check for FastMCP internals
        if hasattr(server, 'app'):
            print("Found app attribute")
            if hasattr(server.app, 'request_handlers'):
                handlers = server.app.request_handlers
                print(f"Request handlers: {list(handlers.keys())}")
                if 'tools/list' in handlers:
                    print("✅ Tools list handler found")
                if 'tools/call' in handlers:
                    print("✅ Tools call handler found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_fastmcp()
