# Contract Intelligence Dashboard with MCP and LangChain

This project provides a dashboard to manage and analyze PDF contracts using a Model Context Protocol (MCP) server and LangChain.

## Features
- **Tabular Metadata**: View essential information like contract name, effective date, client, and amount in a table.
- **Contract Selection**: Use the sidebar to select specific contracts for detailed analysis.
- **MCP Server**: A Python-based MCP server that provides tools for contract processing.
- **LangChain Integration**: Uses LangChain for PDF loading and a mock LLM for chatbot responses.
- **Chatbot**: A built-in chatbot to answer predefined queries about the contracts.

## Project Structure
- `contracts/`: Folder containing sample PDF contracts.
- `mcp_server.py`: The MCP server implementation.
- `dashboard.py`: The Streamlit-based dashboard.
- `generate_contracts.py`: Utility to generate sample PDF files.

## Setup Instructions (VS Code)

1. **Install Dependencies**:
   Open a terminal in VS Code and run:
   ```bash
   pip install reportlab langchain langchain-community langchain-core pypdf mcp streamlit
   ```

2. **Generate Sample Contracts**:
   Run the following command to create the `contracts/` directory and some sample PDFs:
   ```bash
   python generate_contracts.py
   ```

3. **Run the Dashboard**:
   Start the Streamlit dashboard by running:
   ```bash
   streamlit run dashboard.py
   ```
   VS Code should automatically open a browser window with the dashboard. If not, follow the link provided in the terminal (usually `http://localhost:8501`).

## How to use
- Select **"All Contracts"** from the sidebar to see a summary table of all PDF files in the `contracts/` folder.
- Select a specific contract from the dropdown to see its extracted metadata and a basic analysis.
- Use the **Chatbot** in the sidebar to ask questions like "How many contracts are there?" or other general queries.

## Note on MCP Server
The `mcp_server.py` can also be run independently or integrated into MCP-compatible clients like Claude Desktop. For simplicity, the dashboard imports these tools directly, but they are fully compatible with the MCP protocol.

To run it standalone (for testing tools):
```bash
python mcp_server.py
```
