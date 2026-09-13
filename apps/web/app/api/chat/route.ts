import { type NextRequest } from "next/server";

const API_BASE_URL = process.env.AI_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function POST(request: NextRequest) {
  const body = (await request.json()) as { message?: unknown };
  if (typeof body.message !== "string" || !body.message.trim()) {
    return Response.json({ error: "message is required" }, { status: 400 });
  }

  const upstream = await fetch(`${API_BASE_URL}/v1/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: body.message.trim(),
      conversation_id: null,
      tenant_id: "tenant-demo",
      user_id: "user-demo",
    }),
    cache: "no-store",
    signal: request.signal,
  });

  if (!upstream.ok || !upstream.body) {
    return Response.json({ error: "AI service unavailable" }, { status: 502 });
  }

  return new Response(upstream.body, {
    status: upstream.status,
    headers: {
      "Content-Type": upstream.headers.get("content-type") ?? "application/x-ndjson",
      "Cache-Control": "no-store",
    },
  });
}
