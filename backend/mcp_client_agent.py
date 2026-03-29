import asyncio
import sys
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# MCP Server Parameters
server_params = StdioServerParameters(
    command=sys.executable,
    args=[os.path.join(os.path.dirname(os.path.dirname(__file__)), "mcp-server", "mcp_server.py")],
    env=os.environ.copy()
)

class MCPAgent:
    def __init__(self):
        # Verify if OPENAI_API_KEY is available
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            print("WARNING: OPENAI_API_KEY not found in environment variables.")
            print("Please set your OpenAI API key to use the real LLM agent.")

        # Initialize the real LLM with ChatGPT model if key is available, else use a placeholder
        if self.api_key:
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=self.api_key)
        else:
            self.llm = None

    async def run_query(self, query: str, history: list = None):
        if not self.llm:
            return "Error: OPENAI_API_KEY is not set. Please provide a valid API key in your environment variables to use the real ChatGPT-based agent."

        if history is None:
            history = []

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Load tools from MCP server
                tools = await load_mcp_tools(session)

                # Create the agent executor using the real LLM and MCP tools
                agent_executor = create_react_agent(self.llm, tools)

                # Invoke the agent with query and message history
                # We expect response to be a dict containing "messages"
                result = await agent_executor.ainvoke({
                    "messages": history + [HumanMessage(content=query)]
                })

                # Extract the final response content from the agent's messages
                final_message = result["messages"][-1]
                return final_message.content

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
            elif msg["role"] == "assistant" or msg["role"] == "ai":
                lc_history.append(AIMessage(content=msg["content"]))

    try:
        return asyncio.run(agent.run_query(query, lc_history))
    except Exception as e:
        return f"An error occurred while communicating with the agent: {str(e)}"

if __name__ == "__main__":
    # Test
    print(f"User: How many contracts are there?")
    print(f"Agent: {get_agent_response('How many contracts are there?')}")

    print(f"\nUser: Read the content of contract_1.pdf")
    print(f"Agent: {get_agent_response('Read the content of contract_1.pdf')}")
