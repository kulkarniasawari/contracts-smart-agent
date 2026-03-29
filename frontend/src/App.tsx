import { useState, useEffect, useRef } from 'react'
import './App.css'

interface Metadata {
  filename: string;
  name: string;
  effective_date: string;
  client: string;
  amount: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const PREDEFINED_QUESTIONS = [
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
];

function App() {
  const [contracts, setContracts] = useState<string[]>([]);
  const [selectedContract, setSelectedContract] = useState<string>("All Contracts");
  const [metadataList, setMetadataList] = useState<Metadata[]>([]);
  const [selectedMetadata, setSelectedMetadata] = useState<Metadata | null>(null);
  const [analysis, setAnalysis] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchContracts();
  }, []);

  useEffect(() => {
    if (selectedContract === "All Contracts") {
      fetchAllMetadata();
      setSelectedMetadata(null);
      setAnalysis("");
    } else {
      fetchContractDetails(selectedContract);
    }
  }, [selectedContract]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchContracts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/contracts');
      const data = await response.json();
      setContracts(data);
    } catch (error) {
      console.error("Error fetching contracts:", error);
    }
  };

  const fetchAllMetadata = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/contracts/all/metadata');
      const data = await response.json();
      setMetadataList(data);
    } catch (error) {
      console.error("Error fetching all metadata:", error);
    }
  };

  const fetchContractDetails = async (filename: string) => {
    try {
      const metaRes = await fetch(`http://localhost:8000/api/contracts/${filename}/metadata`);
      const metaData = await metaRes.json();
      setSelectedMetadata(metaData);

      const analysisRes = await fetch(`http://localhost:8000/api/contracts/${filename}/analyze`);
      const analysisData = await analysisRes.json();
      setAnalysis(analysisData.analysis);
    } catch (error) {
      console.error("Error fetching contract details:", error);
    }
  };

  const handleSendMessage = async (query: string) => {
    if (!query || query === "Select a question...") return;

    const newMessages: Message[] = [...messages, { role: 'user', content: query }];
    setMessages(newMessages);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, history: messages })
      });
      const data = await response.json();
      setMessages([...newMessages, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <h2>Navigation</h2>
        <div className="form-group">
          <label htmlFor="contract-select">Select a Contract</label>
          <select
            id="contract-select"
            value={selectedContract}
            onChange={(e) => setSelectedContract(e.target.value)}
          >
            <option value="All Contracts">All Contracts</option>
            {contracts.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <hr />
        <h3>Chatbot</h3>
        <div className="form-group">
          <label htmlFor="question-select">General Questions</label>
          <select
            id="question-select"
            onChange={(e) => handleSendMessage(e.target.value)}
            value="Select a question..."
          >
            {PREDEFINED_QUESTIONS.map(q => <option key={q} value={q}>{q}</option>)}
          </select>
        </div>

        <div className="chat-history">
          {messages.map((m, i) => (
            <div key={i} className={`chat-message ${m.role}`}>
              <strong>{m.role === 'user' ? 'User' : 'Assistant'}:</strong>
              <p>{m.content}</p>
            </div>
          ))}
          {isLoading && <div className="chat-message assistant"><em>Agent is thinking...</em></div>}
          <div ref={chatEndRef} />
        </div>

        <form className="chat-input" onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage(inputValue);
        }}>
          <input
            type="text"
            placeholder="Ask about contracts..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
        </form>
      </aside>

      <main className="main-content">
        <header>
          <h1>📄 Contract Intelligence Dashboard</h1>
        </header>

        {selectedContract === "All Contracts" ? (
          <section>
            <h2>Overview of All Contracts</h2>
            <table className="contracts-table">
              <thead>
                <tr>
                  <th>Filename</th>
                  <th>Name</th>
                  <th>Effective Date</th>
                  <th>Client</th>
                </tr>
              </thead>
              <tbody>
                {metadataList.map(m => (
                  <tr key={m.filename}>
                    <td>{m.filename}</td>
                    <td>{m.name}</td>
                    <td>{m.effective_date}</td>
                    <td>{m.client}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        ) : (
          <section>
            <h2>Details for {selectedContract}</h2>
            <div className="details-grid">
              <div className="metadata-card">
                <h3>Metadata</h3>
                <pre>{JSON.stringify(selectedMetadata, null, 2)}</pre>
              </div>
              <div className="analysis-card">
                <h3>Analysis</h3>
                <div className="analysis-text">
                  {analysis.split('\n').map((line, i) => <p key={i}>{line}</p>)}
                </div>
              </div>
            </div>
            <hr />
            <div className="preview-card">
              <h3>Contract Preview (Simplified)</h3>
              {selectedMetadata && (
                <>
                  <div className="info-box">Contract Name: {selectedMetadata.name}</div>
                  <div className="info-box">Effective Date: {selectedMetadata.effective_date}</div>
                  <div className="info-box">Client: {selectedMetadata.client}</div>
                </>
              )}
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
