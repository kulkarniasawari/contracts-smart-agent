import os
import sys

# Add the parent directory and backend directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, "backend"))

from mcp_client_agent import get_agent_response

questions = [
    "How many contracts are currently managed?",
    "List all the contracts available in the system.",
    "What are the metadata details for contract_1.pdf?",
    "Can you provide an analysis of contract_1.pdf?",
    "Who is the client in contract_2.pdf?",
    "What is the effective date of contract_2.pdf?",
    "What is the total amount for contract_3.pdf?",
    "Can you provide an analysis of contract_3.pdf?",
    "Show me the metadata for contract_3.pdf.",
    "Summarize the details of contract_2.pdf."
]

for q in questions:
    print(f"Q: {q}")
    response = get_agent_response(q)
    print(f"A: {response}\n")
