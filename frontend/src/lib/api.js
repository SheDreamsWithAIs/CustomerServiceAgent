export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function chat({ message, userId, threadId, mode }) {
  const url = new URL("/api/v1/chat", API_BASE);
  if (mode) url.searchParams.set("mode", mode);

  const res = await fetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json", accept: "application/json" },
    body: JSON.stringify({ message, user_id: userId, thread_id: threadId }),
  });

  if (!res.ok) {
    let detail = "Request failed";
    try {
      const j = await res.json();
      detail = j?.detail || detail;
    } catch {}
    throw new Error(detail);
  }

  return res.json();
}

export async function chatStream({ message, userId, threadId, mode, onChunk }) {
  const url = new URL("/api/v1/chat/stream", API_BASE);
  if (mode) url.searchParams.set("mode", mode);

  const res = await fetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json", accept: "text/event-stream" },
    body: JSON.stringify({ message, user_id: userId, thread_id: threadId }),
  });
  if (!res.ok || !res.body) {
    let detail = "Request failed";
    try {
      const j = await res.json();
      detail = j?.detail || detail;
    } catch {}
    throw new Error(detail);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let done = false;
  while (!done) {
    const { value, done: d } = await reader.read();
    done = d;
    if (value) {
      const text = decoder.decode(value, { stream: true });
      // Parse SSE lines, accumulate only data: ...
      for (const line of text.split(/\r?\n/)) {
        const m = line.match(/^data:(.*)$/);
        if (m) {
          const data = m[1];
          if (data === "[DONE]") return;
          onChunk?.(data);
        }
      }
    }
  }
}
