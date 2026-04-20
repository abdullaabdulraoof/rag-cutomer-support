import React, { useState, useRef, useEffect } from "react";
import { gsap } from "gsap";
import axios from "axios";

const ChatBox = ({ sessionId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatRef = useRef(null);

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

  // 🔥 Animate messages when added
  useEffect(() => {
    if (chatRef.current) {
      gsap.fromTo(
        chatRef.current.lastChild,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.4 }
      );
    }
  }, [messages]);
  useEffect(() => {
    chatRef.current?.scrollTo({
      top: chatRef.current.scrollHeight,
      behavior: "smooth"
    });
  }, [messages]);


  useEffect(() => {
    if (!sessionId) return;
    setMessages([]);

    async function loadHistory() {
      try {
        const res = await axios.get(
          `http://localhost:8000/history/${sessionId}`
        );
        setMessages(res.data || []);
      } catch (err) {
        console.error(err);
      }
    }

    loadHistory();
  }, [sessionId]);

  const sendMessage = async () => {
    if (!input.trim() || !sessionId) return;

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      { text: userMessage, sender: "user" },
      { text: "", sender: "bot" }
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userMessage,
          sessionId: sessionId,
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let result = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        result += chunk;

        setMessages((prev) => {
          const updated = [...prev];
          if (updated.length > 0) {
            updated[updated.length - 1] = {
              ...updated[updated.length - 1],
              text: result,
            };
          }
          return updated;
        });
      }

      speak(result);

    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };
  return (
    <div className="chat-container">
      <h2>🤖 AI Support Chat</h2>

      <div className="chat-box" ref={chatRef}>
        {messages.map((msg, i) => (
          <div key={sessionId + "-" + i} className={msg.sender === "user" ? "user" : "bot"}>
            <strong>{msg.sender === "user" ? "You" : "AI"}:</strong> {msg.text}
          </div>
        ))}

        {loading && <div className="typing">AI is typing...</div>}
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