import { useState } from 'react';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [prompt, setPrompt] = useState('Explain me the document');
  const [response, setResponse] = useState('');
  const [documentText, setDocumentText] = useState('');
  const [model, setModel] = useState('llama3.2');
  const [mode, setMode] = useState('document');
  const [loading, setLoading] = useState(false);

  async function askAssistant() {
    setLoading(true);
    setResponse('');

    try {
      const payload = {
        model,
        prompt,
        document_text: documentText
      };

      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      console.log(data);

      if (data.error) {
        setResponse(data.error);
      } else {
        setResponse(data.response || JSON.stringify(data));
      }
    } catch (error) {
      setResponse('Error contacting backend: ' + error.message);
    } finally {
      setLoading(false);
    }
  }

  function startVoiceInput() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setResponse('Speech recognition is not supported in this browser.');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setPrompt(transcript);
    };

    recognition.start();
  }

  async function handleDocumentUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/api/document/extract', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      console.log(data);

      if (data.error) {
        setResponse(data.error);
      } else {
        setDocumentText(data.text || '');
        setResponse('Document uploaded successfully. Ask a question about it.');
      }
    } catch (error) {
      setResponse('Upload failed: ' + error.message);
    }
  }

  async function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('prompt', prompt || 'Describe this image in detail.');

    try {
      const res = await fetch('http://localhost:8000/api/vision/analyze', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      console.log(data);

      if (data.error) {
        setResponse(data.error);
      } else {
        setResponse(data.response || JSON.stringify(data));
      }
    } catch (error) {
      setResponse('Upload failed: ' + error.message);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>UltraX AI</h1>
      </header>

      <main className="panel">
        <label>
          Mode
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="text">Text</option>
            <option value="voice">Voice</option>
            <option value="vision">Vision</option>
            <option value="document">Document</option>
          </select>
        </label>

        <label>
          Model
          <select value={model} onChange={(e) => setModel(e.target.value)}>
            <option value="llama3.2">llama3.2</option>
            <option value="llava">llava</option>
            <option value="mistral">mistral</option>
          </select>
        </label>

        <textarea
          rows="8"
          placeholder="Ask anything..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />

        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={askAssistant} disabled={loading} style={{ flex: 1 }}>
            {loading ? 'Thinking...' : 'Ask AI'}
          </button>

          {mode === 'voice' && (
            <button
              type="button"
              onClick={startVoiceInput}
              style={{ flex: 1 }}
            >
              🎤 Voice
            </button>
          )}
        </div>

        {mode === 'document' && (
          <label
            style={{
              display: 'block',
              marginTop: '16px',
              padding: '12px 16px',
              border: '1px solid #475569',
              borderRadius: '10px',
              cursor: 'pointer',
              background: '#0b1220',
              textAlign: 'center'
            }}
          >
            Upload Document
            <input
              type="file"
              accept=".txt,.pdf,.docx"
              hidden
              onChange={handleDocumentUpload}
            />
          </label>
        )}

        {mode === 'vision' && (
          <label
            style={{
              display: 'block',
              marginTop: '16px',
              padding: '12px 16px',
              border: '1px solid #475569',
              borderRadius: '10px',
              cursor: 'pointer',
              background: '#0b1220',
              textAlign: 'center'
            }}
          >
            Upload Image
            <input
              type="file"
              accept="image/*"
              hidden
              onChange={handleImageUpload}
            />
          </label>
        )}

        <div className="response-box" style={{ marginTop: '20px' }}>
          <h3>Assistant Reply</h3>
          <p>{response || 'No response yet'}</p>
        </div>
      </main>
    </div>
  );
}

export default App;
