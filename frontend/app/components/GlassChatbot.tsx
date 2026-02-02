"use client";

import { useEffect, useRef, useState } from "react";

type Msg = {
  role: "user" | "bot";
  text: string;
};

export default function GlassChatbot({
  onSend,
  onOpenChange,
}: {
  onSend: (message: string) => Promise<string>;
  onOpenChange?: (open: boolean) => void;
}) {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "bot",
      text: "Hi 👋 I’m your Todo Assistant. Type: add milk | list | complete 1",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const setOpenBoth = (v: boolean) => {
    setOpen(v);
    onOpenChange?.(v);
  };

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, open]);

  const send = async () => {
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((p) => [...p, { role: "user", text: userMsg }]);
    setLoading(true);

    try {
      const reply = await onSend(userMsg);
      setMessages((p) => [...p, { role: "bot", text: reply }]);
    } catch {
      setMessages((p) => [...p, { role: "bot", text: "❌ Something went wrong" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* ✅ Floating AI button */}
      {!open && (
        <button
          onClick={() => setOpenBoth(true)}
          className="fixed bottom-6 right-6 h-14 w-14 rounded-full
                     bg-gradient-to-br from-yellow-400 to-yellow-600
                     text-black font-bold shadow-xl z-[90]"
        >
          AI
        </button>
      )}

      {/* ✅ Chat window bottom-right */}
      {open && (
        <div
          className="fixed bottom-6 right-6 w-[380px] h-[520px] z-[90]
                     rounded-2xl border border-white/20
                     bg-white/10 backdrop-blur-xl shadow-2xl
                     flex flex-col overflow-hidden"
          role="dialog"
          aria-label="Todo AI Chat"
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-white/20">
            <span className="text-yellow-400 font-semibold">Todo AI</span>

            <div className="flex items-center gap-3">
              <span className="text-[11px] text-white/50">Agent + MCP Tools</span>
              <button
                onClick={() => setOpenBoth(false)}
                className="h-8 w-8 rounded-full bg-white/10 text-white hover:bg-white/20"
                title="Close"
              >
                ×
              </button>
            </div>
          </div>

          {/* Messages */}
          <div
            ref={scrollRef}
            className="flex-1 overflow-y-auto px-4 py-3 text-sm space-y-2 text-white"
          >
            {messages.map((m, i) => (
              <div
                key={i}
                className={m.role === "user" ? "text-right" : "text-left text-gray-200"}
              >
                <span
                  className={
                    m.role === "user"
                      ? "inline-block bg-yellow-500 text-black px-3 py-1 rounded-lg"
                      : "inline-block bg-white/10 px-3 py-1 rounded-lg"
                  }
                >
                  {m.text}
                </span>
              </div>
            ))}
            {loading && <div className="text-left text-gray-400">Thinking…</div>}
          </div>

          {/* Input */}
          <div className="flex gap-2 px-3 py-3 border-t border-white/20">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Type command…"
              className="flex-1 rounded-lg bg-black/40 px-3 py-2 text-white outline-none"
            />
            <button
              onClick={send}
              disabled={loading}
              className="rounded-lg px-4 py-2 bg-yellow-500 text-black font-semibold disabled:opacity-60"
            >
              Send
            </button>
          </div>

          {/* ✅ ChatKit note (as per your screenshot) */}
          <p className="px-4 pb-3 text-[11px] text-white/50">
            ChatKit-style UI (custom). Official ChatKit not used due to App Router incompatibility.
          </p>
        </div>
      )}
    </>
  );
}
