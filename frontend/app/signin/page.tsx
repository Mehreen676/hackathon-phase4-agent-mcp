"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const AUTH_KEY = "todo_user_id";

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState("test-user");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const id = localStorage.getItem(AUTH_KEY);
    if (id) router.replace("/dashboard");
  }, [router]);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    localStorage.setItem(AUTH_KEY, email.trim() || "test-user");

    setTimeout(() => {
      router.push("/dashboard");
    }, 300);
  };

  return (
    <main className="min-h-screen bg-[#0b0f14]">
      {/* ✅ TOP-LEFT TodoApp (sirf ye add hua) */}
      <div className="absolute top-6 left-6 flex items-center gap-2">
        <div className="h-9 w-9 rounded-lg border border-[#1f2937] bg-[#121821] flex items-center justify-center">
          <span className="text-[#f5c16c] font-bold">✎</span>
        </div>
        <span className="text-xl font-bold text-[#f5c16c]">TodoApp</span>
      </div>

      {/* Existing UI SAME */}
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="w-full max-w-md bg-[#121821] border border-[#1f2937] rounded-2xl shadow-2xl p-8">
          <h1 className="text-3xl font-bold text-[#f5c16c]">Sign In</h1>
          <p className="text-gray-400 mt-2">
            Enter your email/username (demo login).
          </p>

          <form onSubmit={onSubmit} className="mt-8 space-y-4">
            <div>
              <label className="text-sm text-gray-300">Email / Username</label>
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-2 w-full rounded-xl bg-[#0b0f14] border border-[#1f2937] px-4 py-3 text-white outline-none focus:border-[#f5c16c]"
                placeholder="mehru@example.com"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl py-3 font-semibold text-black bg-[#f5c16c] hover:brightness-95 transition disabled:opacity-60"
            >
              {loading ? "Signing in..." : "Sign In"}
            </button>

            <p className="text-xs text-gray-500">
              * Demo auth: no password required.
            </p>
          </form>
        </div>
      </div>
    </main>
  );
}
