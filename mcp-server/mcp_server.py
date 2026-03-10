from mcp.server.fastmcp import FastMCP
import os
import sys

# Add the parent directory and mcp-tools directory to sys.path to import tools
# since 'mcp-tools' contains a hyphen and is not a valid python package name
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, "mcp-tools"))

import tools

mcp = FastMCP("Contract Management Server")

# Register tools from the tools module
@mcp.tool()
def list_contracts():
    """List all available contract PDF files."""
    return tools.list_contracts()

@mcp.tool()
def get_contract_metadata(filename: str):
    """Extract metadata from a contract PDF using LangChain."""
    return tools.get_contract_metadata(filename)

@mcp.tool()
def analyze_contract(filename: str):
    """Provide a basic analysis of the contract."""
    return tools.analyze_contract(filename)

@mcp.tool()
def get_contract_text(filename: str):
    """Retrieve the full text content of a contract PDF."""
    return tools.get_contract_text(filename)

@mcp.tool()
def chatbot_query(query: str, selected_contract: str = None):
    """Answer predefined queries using LangChain."""
    return tools.chatbot_query(query, selected_contract)

if __name__ == "__main__":
    mcp.run()
