"use client";

import { useEffect, useState } from "react";

type Msg = {
  role: "user" | "bot";
  text: string;
};

export default function ChatKitPage() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(false);
  const [mounted, setMounted] = useState(false);

  // 🔒 Fix hydration mismatch
  useEffect(() => {
    setMounted(true);
  }, []);

  async function send() {
    if (!input.trim() || loading) return;

    const userMsg: Msg = { role: "user", text: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/chatkit/proxy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.text }),
      });

      const data = await res.json();

      const botText =
        data?.reply ||
        data?.message ||
        JSON.stringify(data, null, 2);

      setMessages((m) => [...m, { role: "bot", text: botText }]);
    } catch (e: any) {
      setMessages((m) => [
        ...m,
        { role: "bot", text: "Error: " + e.message },
      ]);
    } finally {
      setLoading(false);
    }
  }

  if (!mounted) return null;

  return (
    <div style={{ padding: 24, maxWidth: 900 }}>
      <h2>ChatKit UI (via Next Proxy)</h2>

      <div
        style={{
          border: "1px solid #ddd",
          padding: 12,
          minHeight: 260,
          whiteSpace: "pre-wrap",
          marginBottom: 12,
        }}
      >
        {messages.map((m, i) => (
          <div key={i}>
            <b>{m.role === "user" ? "You" : "Bot"}:</b> {m.text}
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          style={{ flex: 1, padding: 8 }}
          placeholder="Type a command..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button onClick={send} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>

      <p style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
        Endpoint: <code>/api/chatkit/proxy</code> → FastAPI <code>/api/demo/chat</code>
      </p>
    </div>
  );
}
