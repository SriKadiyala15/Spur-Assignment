import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    { sender: "ai", text: "Hi! How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  const hasMessages = messages.length > 1;

  // Auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Load chat history on refresh
  useEffect(() => {
    const loadHistory = async () => {
      const sessionId = localStorage.getItem("sessionId");

      if (!sessionId) return;

      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/chat/history/${sessionId}`
        );

        if (response.data.length > 0) {
          setMessages(response.data);
        }
      } catch (error) {
        console.log("History load failed:", error);
      }
    };

    loadHistory();
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    const currentInput = input;
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat/message",
        {
          message: currentInput,
          sessionId: localStorage.getItem("sessionId")
        }
      );

      localStorage.setItem("sessionId", response.data.sessionId);

      const aiMessage = {
        sender: "ai",
        text: response.data.reply
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "Error connecting to server." }
      ]);
    }

    setLoading(false);
  };

  return (
    <div className={`chat-container ${hasMessages ? "active-chat" : "initial-chat"}`}>
      {!hasMessages && (
        <>
          <h1>AI Support Agent</h1>
          <p className="subtitle">How can I help you today?</p>
        </>
      )}

      {hasMessages && (
        <>
          <h1>AI Support Agent</h1>

          <div className="chat-box">
            {messages.map((msg, index) => (
              <div key={index} className={msg.sender}>
                {msg.text}
              </div>
            ))}

            {loading && <div className="ai">Typing...</div>}

            <div ref={chatEndRef}></div>
          </div>
        </>
      )}

      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask something..."
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;