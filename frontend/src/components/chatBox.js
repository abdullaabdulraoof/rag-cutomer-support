import React, { useState } from "react";

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // 🎤 Voice input
  const startListening = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
      const speechText = event.results[0][0].transcript;
      setInput(speechText);
    };
  };

  // 🔊 Text to speech
  const speak = (text) => {
    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
  };

  // 🚀 Streaming chat
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    // Add user message
    setMessages((prev) => [...prev, { text: userMessage, sender: "user" }]);

    setInput("");
    setLoading(true);

    // Add empty AI message
    setMessages((prev) => [...prev, { text: "", sender: "bot" }]);

    try {
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userMessage }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let result = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        result += chunk;

        // 🔥 Update last bot message (streaming effect)
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            text: result,
            sender: "bot",
          };
          return updated;
        });
      }

      speak(result); // 🔊 speak response
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="chat-container">
      <h2>🤖 AI Support Chat</h2>

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={msg.sender}>
            <p style={{ color: msg.sender === "user" ? "blue" : "green" }}>
              {msg.text}
            </p>
          </div>
        ))}

        {loading && <p style={{ color: "gray" }}>Thinking...</p>}
      </div>

      <div className="input-box">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
        />

        <button onClick={sendMessage}>Send</button>
        <button onClick={startListening}>🎤</button>
      </div>
    </div>
  );
};

export default ChatBox;