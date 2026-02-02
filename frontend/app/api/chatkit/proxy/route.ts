import { NextResponse } from "next/server";

export const runtime = "nodejs";

export async function POST(req: Request) {
  try {
    // ✅ JSON correctly parse
    const body = await req.json();

    const apiBase =
      process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

    const upstream = `${apiBase}/api/demo/chat`;

    const r = await fetch(upstream, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await r.text();

    return new NextResponse(data, {
      status: r.status,
      headers: {
        "Content-Type": r.headers.get("content-type") || "application/json",
      },
    });
  } catch (e: any) {
    return NextResponse.json(
      { error: e?.message || "proxy failed" },
      { status: 500 }
    );
  }
}
