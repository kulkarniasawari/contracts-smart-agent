import streamlit as st
import pandas as pd
import os
from mcp_server import list_contracts, get_contract_metadata, analyze_contract, chatbot_query

st.set_page_config(page_title="Contract Intelligence Dashboard", layout="wide")

st.title("📄 Contract Intelligence Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
contracts = list_contracts()
selected_contract = st.sidebar.selectbox("Select a Contract", ["All Contracts"] + contracts)

# Chatbot in Sidebar
st.sidebar.divider()
st.sidebar.subheader("Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.sidebar.chat_message(message["role"]):
        st.sidebar.markdown(message["content"])

if prompt := st.sidebar.chat_input("Ask about contracts..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.sidebar.chat_message("user"):
        st.sidebar.markdown(prompt)

    with st.sidebar.chat_message("assistant"):
        # Use MCP tool for chatbot
        if "list" in prompt.lower() or "how many" in prompt.lower():
            response = f"There are {len(contracts)} contracts available: " + ", ".join(contracts)
        else:
            response = chatbot_query(prompt, selected_contract if selected_contract != "All Contracts" else None)

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
    st.info(f"Amount: {metadata['amount']}")
