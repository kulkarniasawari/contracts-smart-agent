import os
import sys

# Add the parent directory and mcp-tools directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, "mcp-tools"))

from tools import list_contracts, get_contract_metadata, analyze_contract, chatbot_query, get_contract_text

print("Listing contracts:")
contracts = list_contracts()
print(contracts)

if contracts:
    print("\nMetadata for first contract:")
    metadata = get_contract_metadata(contracts[0])
    print(metadata)

    print("\nAnalysis for first contract:")
    analysis = analyze_contract(contracts[0])
    print(analysis)

    print("\nText content for first contract (first 200 chars):")
    text = get_contract_text(contracts[0])
    print(text[:200] if isinstance(text, str) else text)

print("\nChatbot query:")
response = chatbot_query("What can you do?")
print(response)
