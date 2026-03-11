import os
import datetime
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.fake import FakeListLLM

CONTRACTS_DIR = "contracts"
ACTIVITY_LOG_FILE = "activity_log.txt"

def log_activity(description: str):
    """Log an activity with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {description}\n"
    with open(ACTIVITY_LOG_FILE, "a") as f:
        f.write(log_entry)

def list_contracts():
    """List all available contract PDF files."""
    log_activity("Listed all contracts.")
    files = [f for f in os.listdir(CONTRACTS_DIR) if f.endswith(".pdf")]
    return files

def get_contract_metadata(filename: str):
    """Extract metadata from a contract PDF using LangChain."""
    log_activity(f"Extracted metadata for {filename}.")
    filepath = os.path.join(CONTRACTS_DIR, filename)
    if not os.path.exists(filepath):
        return {"error": "File not found"}

    loader = PyPDFLoader(filepath)
    docs = loader.load()
    text = "\n".join([doc.page_content for doc in docs])

    # Simple extraction logic (in a real app, use an LLM with LangChain)
    lines = text.split("\n")
    metadata = {
        "filename": filename,
        "name": "Unknown",
        "effective_date": "Unknown",
        "client": "Unknown",
        "amount": "Unknown"
    }

    for line in lines:
        if "Contract Name:" in line:
            metadata["name"] = line.split("Contract Name:")[1].strip()
        elif "Effective Date:" in line:
            metadata["effective_date"] = line.split("Effective Date:")[1].strip()
        elif "Client:" in line:
            metadata["client"] = line.split("Client:")[1].strip()
        elif "Total Amount:" in line:
            metadata["amount"] = line.split("Total Amount:")[1].strip()

    return metadata

def analyze_contract(filename: str):
    """Provide a basic analysis of the contract."""
    log_activity(f"Analyzed contract: {filename}.")
    metadata = get_contract_metadata(filename)
    if "error" in metadata:
        return metadata

    analysis = f"Analysis for {filename}:\n"
    analysis += f"- The contract is with {metadata['client']}.\n"
    analysis += f"- It became effective on {metadata['effective_date']}.\n"
    analysis += f"- The total value is {metadata['amount']}.\n"
    analysis += "- Purpose: " + ("Software related" if "Software" in metadata["name"] or "Cloud" in metadata["name"] else "General services")

    return analysis

def get_contract_text(filename: str):
    """Retrieve the full text content of a contract PDF."""
    log_activity(f"Retrieved text for {filename}.")
    filepath = os.path.join(CONTRACTS_DIR, filename)
    if not os.path.exists(filepath):
        return {"error": "File not found"}

    loader = PyPDFLoader(filepath)
    docs = loader.load()
    text = "\n".join([doc.page_content for doc in docs])
    return text

def chatbot_query(query: str, selected_contract: str = None):
    """Answer predefined queries using LangChain."""
    log_activity(f"Chatbot query: {query}")
    responses = [
        "I can help you with contract analysis.",
        "The selected contract is a service agreement.",
        "You can find the effective date in the metadata section.",
        "This project uses MCP and LangChain for contract processing."
    ]
    fake_llm = FakeListLLM(responses=responses)

    prompt = PromptTemplate.from_template("Answer the following query about contracts: {query}")

    # Using LCEL (LangChain Expression Language)
    chain = prompt | fake_llm
    response = chain.invoke({"query": query})

    return response

def get_notifications():
    """Retrieve all logged activities as notifications."""
    if not os.path.exists(ACTIVITY_LOG_FILE):
        return []
    with open(ACTIVITY_LOG_FILE, "r") as f:
        notifications = f.readlines()
    return [n.strip() for n in notifications]
