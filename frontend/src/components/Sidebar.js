import React from "react";

const Sidebar = ({ sessions, currentSession, setSession }) => {
  return (
    <div className="sidebar">
    <button
  className="new-chat-btn"
  onClick={() => {
  const newSession = Date.now().toString();
  setSession(newSession);
}}
>
  + New Chat
</button>

      <div className="session-list">
        {sessions.map((session) => (
          <div
            key={session}
            className={`session-item ${
              currentSession === session ? "active" : ""
            }`}
            onClick={() => setSession(session)}
          >
            Chat {session.slice(-4)}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;