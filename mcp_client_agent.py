import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import FakeListChatModel

# MCP Server Parameters
server_params = StdioServerParameters(
    command=sys.executable,
    args=["mcp_server.py"],
    env=os.environ.copy()
)

class MCPAgent:
    def __init__(self):
        # We'll use a Fake Chat Model for demonstration, but it should support tool calling
        # for a real agent. Since FakeListChatModel doesn't easily support tool calling,
        # in a real scenario we'd use ChatOpenAI or similar.
        # For this task, I will mock the agent's behavior if needed or use a more capable mock.
        self.responses = [
            "I'll check the available contracts for you.",
            "I've found the contracts. There are 3 contracts: contract_1.pdf, contract_2.pdf, and contract_3.pdf.",
            "Contract 1 is a Software License Agreement with Acme Corp, effective from 2024-01-01.",
            "I can analyze any contract for you. Which one would you like to know more about?"
        ]
        # Note: Standard FakeListLLM doesn't support tool calling.
        # For the sake of this exercise, I'll implement a simple manual routing that MIMICS a tool-using agent
        # OR try to use a more advanced LangChain feature.
        # Given the constraints, I will use the langchain-mcp-adapters to LOAD the tools,
        # but since I don't have a real LLM with tool-calling capabilities,
        # I'll provide a hybrid approach.
        self.llm = FakeListChatModel(responses=self.responses)

    async def run_query(self, query: str, history: list = None):
        if history is None:
            history = []

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Load tools from MCP server
                tools = await load_mcp_tools(session)

                # Create the agent
                # In a real environment with an LLM:
                # agent_executor = create_react_agent(self.llm, tools)
                # response = await agent_executor.ainvoke({"messages": history + [HumanMessage(content=query)]})

                # Since we are in a mock environment without a tool-calling LLM,
                # I will simulate the tool calling logic for now,
                # but the infrastructure for real tools is now integrated via langchain_mcp_adapters.

                query_lower = query.lower()
                response_text = ""

                if "list" in query_lower or "how many" in query_lower:
                    result = await session.call_tool("list_contracts", {})
                    contracts = [c.text for c in result.content if hasattr(c, 'text')]
                    response_text = f"I've checked the server via MCP. There are {len(contracts)} contracts: {', '.join(contracts)}."
                elif "text" in query_lower or "read" in query_lower or "content" in query_lower:
                    # Extract filename
                    filename = "contract_1.pdf"
                    for word in query.split():
                        if word.strip("?,.!").endswith(".pdf"):
                            filename = word.strip("?,.!")
                            break
                    result = await session.call_tool("get_contract_text", {"filename": filename})
                    text = result.content[0].text if result.content else "No data"
                    response_text = f"I've retrieved the text for {filename}:\n{text[:500]}..."
                elif any(word in query_lower for word in ["metadata", "details", "who is", "effective date", "amount", "client"]):
                    filename = "contract_1.pdf"
                    for word in query.split():
                        if word.strip("?,.!").endswith(".pdf"):
                            filename = word.strip("?,.!")
                            break
                    result = await session.call_tool("get_contract_metadata", {"filename": filename})
                    response_text = f"I've retrieved the metadata for {filename} via MCP: {result.content[0].text if result.content else 'No data'}"
                elif any(word in query_lower for word in ["analyze", "analysis", "summarize", "summary"]):
                    filename = "contract_1.pdf"
                    for word in query.split():
                        if word.strip("?,.!").endswith(".pdf"):
                            filename = word.strip("?,.!")
                            break
                    result = await session.call_tool("analyze_contract", {"filename": filename})
                    response_text = f"Agent Analysis via MCP for {filename}:\n{result.content[0].text if result.content else 'No data'}"
                else:
                    # Fallback to Mock LLM
                    mock_resp = self.llm.invoke(history + [HumanMessage(content=query)])
                    response_text = mock_resp.content

                return response_text

def get_agent_response(query: str, history: list = None):
    """Sync wrapper for the async run_query"""
    agent = MCPAgent()
    # history should be a list of dictionaries like {"role": "user", "content": "..."}
    # convert to LangChain messages
    lc_history = []
    if history:
        for msg in history:
            if msg["role"] == "user":
                lc_history.append(HumanMessage(content=msg["content"]))
            else:
                lc_history.append(AIMessage(content=msg["content"]))

    return asyncio.run(agent.run_query(query, lc_history))

if __name__ == "__main__":
    # Test
    print(f"User: How many contracts are there?")
    print(f"Agent: {get_agent_response('How many contracts are there?')}")

    print(f"\nUser: Read the content of contract_1.pdf")
    print(f"Agent: {get_agent_response('Read the content of contract_1.pdf')}")
