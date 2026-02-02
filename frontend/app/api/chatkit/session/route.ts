import { NextResponse } from "next/server";

export async function POST() {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      { error: "Missing OPENAI_API_KEY in frontend env" },
      { status: 500 }
    );
  }

  // ChatKit expects a client_secret from OpenAI Realtime Sessions.
  // This call is made server-side (safe).
  const res = await fetch("https://api.openai.com/v1/realtime/sessions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-4o-mini-realtime-preview",
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    return NextResponse.json(
      { error: "Failed to create realtime session", details: data },
      { status: 500 }
    );
  }

  return NextResponse.json({ client_secret: data.client_secret });
}
