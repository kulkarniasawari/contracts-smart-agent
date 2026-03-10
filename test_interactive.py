from mcp_client_agent import get_agent_response

def test_interactive_chat():
    history = []

    # Turn 1
    query1 = "How many contracts are there?"
    print(f"User: {query1}")
    response1 = get_agent_response(query1, history)
    print(f"Agent: {response1}\n")
    history.append({"role": "user", "content": query1})
    history.append({"role": "assistant", "content": response1})

    # Turn 2
    query2 = "Tell me about the first one."
    print(f"User: {query2}")
    # Note: In our current simulated agent, we extract filename from query.
    # Since 'first one' doesn't contain a filename, it might fallback or we can see how it handles it.
    response2 = get_agent_response(query2, history)
    print(f"Agent: {response2}\n")
    history.append({"role": "user", "content": query2})
    history.append({"role": "assistant", "content": response2})

    # Turn 3
    query3 = "What is the full text of contract_2.pdf?"
    print(f"User: {query3}")
    response3 = get_agent_response(query3, history)
    print(f"Agent: {response3}\n")
    history.append({"role": "user", "content": query3})
    history.append({"role": "assistant", "content": response3})

if __name__ == "__main__":
    test_interactive_chat()
