import React, { useState } from "react";
import axios from "axios";

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const startListening = () => {
  const recognition = new window.webkitSpeechRecognition();

  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = (event) => {
    const speechText = event.results[0][0].transcript;
    setInput(speechText);
  };
};
const speak = (text) => {
  const speech = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(speech);
};
const sendMessage = async () => {
  if (!input.trim()) return;

  const userMessage = { sender: "user", text: input };
  setMessages((prev) => [...prev, userMessage]);

  setLoading(true); // 🔥 start loading

  try {
    const res = await axios.post("http://localhost:5000/api/chat", {
      question: input,
    });

    const botMessage = {
      sender: "bot",
      text: res.data.data.answer,
      sources: res.data.data.sources,
    };
    speak(res.data.data.answer);
    setMessages((prev) => [...prev, botMessage]);

  } catch (err) {
    console.error(err);
  }

  setLoading(false); // 🔥 stop loading
  setInput("");
};

  return (
    <div className="chat-container ">
      <h2>🤖 AI Support Chat</h2>

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={msg.sender}>
            <p>{msg.text}</p>
            {loading && <p className="bot">Thinking...</p>}

            {msg.sources && (
              <small>Sources: {msg.sources.join(", ")}</small>
            )}
          </div>
        ))}
      </div>

      <div className="input-box">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={sendMessage}>Send</button>
        <button onClick={startListening}>🎤</button>
      </div>
    </div>
  );
};

export default ChatBox;