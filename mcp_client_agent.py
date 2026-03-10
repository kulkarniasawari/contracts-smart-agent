import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_community.llms.fake import FakeListLLM

# MCP Server Parameters
server_params = StdioServerParameters(
    command=sys.executable,
    args=["mcp_server.py"],
    env=os.environ.copy()
)

class MCPAgent:
    def __init__(self):
        # Mock LLM responses
        self.responses = [
            "I'll check the available contracts for you. There are 3 contracts: contract_1.pdf, contract_2.pdf, and contract_3.pdf.",
            "Contract 1 is a Software License Agreement with Acme Corp, effective from 2024-01-01.",
            "I can analyze any contract for you. Which one would you like to know more about?"
        ]
        self.llm = FakeListLLM(responses=self.responses)

    async def run_query(self, query: str, context: str = None):
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Extract filename from query if present
                filename_from_query = None
                words = query.split()
                for word in words:
                    clean_word = word.strip("?,.!")
                    if clean_word.lower().endswith(".pdf"):
                        filename_from_query = clean_word
                        break

                # Determine which filename to use
                filename = filename_from_query or (context if context and context != "All Contracts" else "contract_1.pdf")

                # Check if it's a tool-related query
                query_lower = query.lower()
                if "list" in query_lower or "how many" in query_lower:
                    # Call MCP tool
                    result = await session.call_tool("list_contracts", {})
                    contracts = [c.text for c in result.content if hasattr(c, 'text')]
                    response = f"I've checked the server via MCP. There are {len(contracts)} contracts: {', '.join(contracts)}."
                elif any(word in query_lower for word in ["metadata", "tell me about", "details", "who is", "effective date", "amount", "client"]):
                    result = await session.call_tool("get_contract_metadata", {"filename": filename})
                    response = f"I've retrieved the metadata for {filename} via MCP: {result.content[0].text if result.content else 'No data'}"
                elif any(word in query_lower for word in ["analyze", "analysis", "summarize", "summary"]):
                    result = await session.call_tool("analyze_contract", {"filename": filename})
                    response = f"Agent Analysis via MCP for {filename}:\n{result.content[0].text if result.content else 'No data'}"
                else:
                    # Fallback to Mock LLM
                    response = self.llm.invoke(query)

                return response

def get_agent_response(query: str, context: str = None):
    """Sync wrapper for the async run_query"""
    agent = MCPAgent()
    return asyncio.run(agent.run_query(query, context))

if __name__ == "__main__":
    # Test
    print(f"User: How many contracts are there?")
    print(f"Agent: {get_agent_response('How many contracts are there?')}")
