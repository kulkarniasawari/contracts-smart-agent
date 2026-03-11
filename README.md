# Contract Intelligence Dashboard with MCP and LangChain

This project provides a dashboard to manage and analyze PDF contracts using a Model Context Protocol (MCP) server and LangChain.

## Features
- **Tabular Metadata**: View essential information like contract name, effective date, client, and amount in a table.
- **Contract Selection**: Use the sidebar to select specific contracts for detailed analysis.
- **MCP Server**: A Python-based MCP server built with FastMCP that provides tools for contract processing.
- **LangChain & LangGraph Integration**: Uses LangChain for PDF loading and LangGraph with ChatOpenAI (GPT-4o) for intelligent agent-based contract analysis.
- **Chatbot**: A stateful, multi-turn chatbot that uses the MCP agent to answer complex queries about the contracts.
- **Modern UI**: A React-based frontend with a FastAPI backend.

## Project Structure
- `backend/`: Contains the FastAPI application (`backend_app.py`) and the MCP client agent (`mcp_client_agent.py`).
- `mcp-server/`: Contains the FastMCP server implementation (`mcp_server.py`).
- `mcp-tools/`: Centralized tool logic (`tools.py`) shared by the MCP server and Streamlit dashboard.
- `frontend/`: React-based frontend dashboard (Vite project).
- `contracts/`: Folder containing sample PDF contracts.
- `tests/`: Test suites for verifying MCP tools and agent functionality.
- `dashboard.py`: Streamlit-based dashboard.
- `generate_contracts.py`: Utility to generate sample PDF files for testing.

## Setup Instructions

1. **Install Python Dependencies**:
   ```bash
   pip install reportlab langchain langchain-community pypdf mcp langchain-mcp-adapters langgraph langchain-openai streamlit fastapi uvicorn pandas
   ```

2. **Set Environment Variables**:
   Set your OpenAI API key to use the chatbot features:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. **Generate Sample Contracts**:
   ```bash
   python generate_contracts.py
   ```

4. **Install Frontend Dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## Running the Application

To run the modern React-based dashboard, you need to start both the backend and the frontend:

1. **Start the Backend**:
   ```bash
   python backend/backend_app.py
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
