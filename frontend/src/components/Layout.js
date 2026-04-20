import React, { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import ChatBox from "./chatBox";

const Layout = () => {
  const [sessions, setSessions] = useState(() => {
    return JSON.parse(localStorage.getItem("sessions")) || [];
  });

  const [currentSession, setCurrentSession] = useState("");

  // 🔥 Initialize first session
  useEffect(() => {
    if (sessions.length === 0) {
      const newSession = Date.now().toString();
      setSessions([newSession]);
      setCurrentSession(newSession);
    } else {
      setCurrentSession(sessions[0]);
    }
  }, []);

  // 🔥 Persist sessions
  useEffect(() => {
    localStorage.setItem("sessions", JSON.stringify(sessions));
  }, [sessions]);

  // 🔥 FIXED FUNCTION
  const setSession = (id) => {
    setSessions((prev) => {
      if (!prev.includes(id)) {
        return [id, ...prev]; // add new session
      }
      return prev;
    });

    setCurrentSession(id);
  };

  return (
    <div style={{ display: "flex" }}>
      <Sidebar
        sessions={sessions}
        currentSession={currentSession}
        setSession={setSession}
      />

      {currentSession && <ChatBox sessionId={currentSession} />}
    </div>
  );
};

export default Layout;