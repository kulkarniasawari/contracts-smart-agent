from mcp_server import list_contracts, get_contract_metadata, analyze_contract, chatbot_query, get_contract_text

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
