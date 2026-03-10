# Contract Intelligence Dashboard with MCP and LangChain

This project provides a dashboard to manage and analyze PDF contracts using a Model Context Protocol (MCP) server and LangChain.

## Features
- **Tabular Metadata**: View essential information like contract name, effective date, client, and amount in a table.
- **Contract Selection**: Use the sidebar to select specific contracts for detailed analysis.
- **MCP Server**: A Python-based MCP server that provides tools for contract processing.
- **LangChain Integration**: Uses LangChain for PDF loading and a mock LLM for chatbot responses.
- **Chatbot**: A built-in chatbot to answer predefined queries about the contracts.
- **Modern UI**: A React-based frontend with a FastAPI backend.

## Project Structure
- `contracts/`: Folder containing sample PDF contracts.
- `mcp_server.py`: The MCP server implementation.
- `mcp_client_agent.py`: Agent that communicates with the MCP server.
- `backend_app.py`: FastAPI backend that exposes MCP tools as REST endpoints.
- `frontend/`: React-based frontend dashboard.
- `dashboard.py`: Legacy Streamlit-based dashboard.
- `generate_contracts.py`: Utility to generate sample PDF files.

## Setup Instructions

1. **Install Python Dependencies**:
   ```bash
   pip install reportlab langchain langchain-community langchain-core pypdf mcp fastapi uvicorn
   ```

2. **Generate Sample Contracts**:
   ```bash
   python generate_contracts.py
   ```

3. **Install Frontend Dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## Running the Application

To run the modern React-based dashboard, you need to start both the backend and the frontend:

1. **Start the Backend**:
   ```bash
   python backend_app.py
   ```
   The backend will run on `http://localhost:8000`.

2. **Start the Frontend**:
   In a new terminal:
   ```bash
   cd frontend
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`.

### (Optional) Legacy Streamlit Dashboard
If you still want to use the Streamlit dashboard:
```bash
pip install streamlit
streamlit run dashboard.py
```

## How to use
- Select **"All Contracts"** from the sidebar to see a summary table of all PDF files in the `contracts/` folder.
- Select a specific contract from the dropdown to see its extracted metadata and a basic analysis.
- Use the **Chatbot** in the sidebar to ask questions like "How many contracts are there?" or other general queries.

## Note on MCP Server
The `mcp_server.py` can also be run independently or integrated into MCP-compatible clients like Claude Desktop. For simplicity, the dashboard (via `backend_app.py`) communicates with it using the MCP protocol via `mcp_client_agent.py`.
