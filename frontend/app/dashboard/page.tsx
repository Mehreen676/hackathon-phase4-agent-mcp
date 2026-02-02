"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import GlassChatbot from "../components/GlassChatbot";

type Task = {
  id: number;
  user_id: string;
  title: string;
  completed: boolean;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";
const AUTH_KEY = "todo_user_id";

export default function DashboardPage() {
  const router = useRouter();

  const [userId, setUserId] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  const [newTitle, setNewTitle] = useState("");
  const [creating, setCreating] = useState(false);

  // ✅ chatbot open => dashboard shift right
  const [chatOpen, setChatOpen] = useState(false);

  // Auth guard
  useEffect(() => {
    const id = localStorage.getItem(AUTH_KEY);
    if (!id) {
      router.replace("/signin");
      return;
    }
    setUserId(id);
  }, [router]);

  const fetchTasks = async (id: string) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/${encodeURIComponent(id)}/tasks/`, {
        cache: "no-store",
      });
      const data = await res.json().catch(() => []);
      setTasks(Array.isArray(data) ? data : []);
    } catch {
      setTasks([]);
      toast.error("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (userId) fetchTasks(userId);
  }, [userId]);

  // ADD
  const createTask = async () => {
    if (!newTitle.trim()) return;

    setCreating(true);
    try {
      const title = newTitle.trim();
      const res = await fetch(`${API_BASE}/api/${encodeURIComponent(userId)}/tasks/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      });

      if (!res.ok) {
        toast.error("Task add failed");
        return;
      }

      toast.success(`Task added: ${title}`);
      setNewTitle("");
      await fetchTasks(userId);
    } catch {
      toast.error("Network error");
    } finally {
      setCreating(false);
    }
  };

  // COMPLETE
  const toggleComplete = async (id: number) => {
    try {
      const res = await fetch(
        `${API_BASE}/api/${encodeURIComponent(userId)}/tasks/${id}/complete/`,
        { method: "PATCH" }
      );

      if (!res.ok) {
        toast.error("Task update failed");
        return;
      }

      toast.success(`Task completed (#${id})`);
      await fetchTasks(userId);
    } catch {
      toast.error("Network error");
    }
  };

  // DELETE
  const deleteTask = async (id: number) => {
    try {
      const res = await fetch(`${API_BASE}/api/${encodeURIComponent(userId)}/tasks/${id}/`, {
        method: "DELETE",
      });

      if (!res.ok) {
        toast.error("Task delete failed");
        return;
      }

      toast.success(`Task deleted (#${id})`);
      await fetchTasks(userId);
    } catch {
      toast.error("Network error");
    }
  };

  // Chatbot → backend /chat
  const sendToBot = async (message: string) => {
    const msg = (message || "").trim();
    if (!msg) return "Type a command (e.g., add milk, list).";

    try {
      const res = await fetch(`${API_BASE}/api/${encodeURIComponent(userId)}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg }),
      });

      const data = await res.json().catch(() => ({}));
      const reply = typeof (data as any)?.reply === "string" ? (data as any).reply : "OK";

      await fetchTasks(userId);

      const lower = msg.toLowerCase();
      if (lower.startsWith("add ")) toast.success("Task added");
      else if (lower.startsWith("delete ")) toast.success("Task deleted");
      else if (lower.startsWith("complete ")) toast.success("Task completed");

      return reply;
    } catch {
      toast.error("Chat failed");
      return "❌ Chat failed";
    }
  };

  const signOut = () => {
    localStorage.removeItem(AUTH_KEY);
    router.push("/signin");
  };

  return (
    <main className="min-h-screen bg-[#0b0f14] px-6 py-10">
      {/* ✅ Sign Out ALWAYS top-right corner */}
      <button
        onClick={signOut}
        className="fixed top-8 right-10 z-[60] text-gray-300 hover:text-white"
      >
        Sign Out
      </button>

      {/* ✅ Page content; shift when chat opens */}
      <div className={`transition-all duration-200 ${chatOpen ? "lg:pr-[420px]" : ""}`}>
        <div className="mx-auto max-w-5xl">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-[#f5c16c]">My Tasks</h1>
            <p className="text-sm text-gray-400 mt-1">
              Signed in as <span className="text-gray-200">{userId}</span>
            </p>
          </div>

          {/* Add */}
          <div className="flex gap-3 mb-8">
            <input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="New task..."
              className="w-96 px-4 py-3 rounded bg-[#121821] text-white"
            />
            <button
              onClick={createTask}
              disabled={creating}
              className="px-6 py-3 rounded bg-[#f5c16c] text-black font-semibold disabled:opacity-60"
            >
              {creating ? "Adding..." : "Add"}
            </button>
          </div>

          {/* List */}
          {loading ? (
            <p className="text-gray-400">Loading…</p>
          ) : tasks.length === 0 ? (
            <p className="text-gray-400">No tasks yet.</p>
          ) : (
            <div className="space-y-3">
              {tasks.map((t) => (
                <div
                  key={t.id}
                  className="flex justify-between items-center bg-[#121821] px-5 py-4 rounded"
                >
                  <span className={t.completed ? "line-through text-gray-400" : "text-white"}>
                    {t.id}. {t.title}
                  </span>

                  {/* ✅ buttons clickable: no overlay */}
                  <div className="flex gap-2">
                    <button
                      type="button"
                      onClick={() => toggleComplete(t.id)}
                      className="px-3 py-1 bg-green-600 text-xs rounded"
                    >
                      Complete
                    </button>
                    <button
                      type="button"
                      onClick={() => deleteTask(t.id)}
                      className="px-3 py-1 bg-red-600 text-xs rounded"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ✅ Floating chatbot (self-contained) */}
      <GlassChatbot onSend={sendToBot} onOpenChange={setChatOpen} />
    </main>
  );
}
