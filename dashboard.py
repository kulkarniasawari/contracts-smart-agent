import streamlit as st
import pandas as pd
import os
from mcp_server import list_contracts, get_contract_metadata, analyze_contract
from mcp_client_agent import get_agent_response

st.set_page_config(page_title="Contract Intelligence Dashboard", layout="wide")

st.title("📄 Contract Intelligence Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
contracts = list_contracts()
selected_contract = st.sidebar.selectbox("Select a Contract", ["All Contracts"] + contracts)

# Chatbot in Sidebar
st.sidebar.divider()
st.sidebar.subheader("Chatbot")

# Predefined Questions
predefined_questions = [
    "Select a question...",
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

selected_question = st.sidebar.selectbox("General Questions", predefined_questions)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.sidebar.chat_message(message["role"]):
        st.sidebar.markdown(message["content"])

prompt = st.sidebar.chat_input("Ask about contracts...")

# Handle predefined question selection
if selected_question != "Select a question...":
    # Check if this was the last question asked to avoid recursion/re-runs
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != selected_question:
        prompt = selected_question

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.sidebar.chat_message("user"):
        st.sidebar.markdown(prompt)

    with st.sidebar.chat_message("assistant"):
        # Use MCP Agent for chatbot
        with st.spinner("Agent is thinking..."):
            # Pass the message history to the agent for "free flowing" conversation
            response = get_agent_response(prompt, st.session_state.messages[:-1])
        st.sidebar.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


# Main Content
if selected_contract == "All Contracts":
    st.header("Overview of All Contracts")
    data = []
    for c in contracts:
        metadata = get_contract_metadata(c)
        data.append(metadata)

    df = pd.DataFrame(data)
    if 'amount' in df.columns:
        df = df.drop(columns=['amount'])
    st.table(df)

else:
    st.header(f"Details for {selected_contract}")

    col1, col2 = st.columns(2)

    metadata = get_contract_metadata(selected_contract)

    with col1:
        st.subheader("Metadata")
        st.json(metadata)

    with col2:
        st.subheader("Analysis")
        analysis = analyze_contract(selected_contract)
        st.write(analysis)

    st.divider()
    st.subheader("Contract Preview (Simplified)")
    # Just show the metadata in a nice way
    st.info(f"Contract Name: {metadata['name']}")
    st.info(f"Effective Date: {metadata['effective_date']}")
    st.info(f"Client: {metadata['client']}")
