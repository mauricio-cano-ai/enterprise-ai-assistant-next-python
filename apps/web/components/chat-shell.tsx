"use client";

import { useRef, useState } from "react";
import type { Citation } from "@/lib/chat-types";
import { parseNdjsonStream } from "@/lib/stream";
import { ChatInput } from "./chat-input";
import { StreamedAnswer } from "./streamed-answer";

export function ChatShell() {
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [status, setStatus] = useState<"idle" | "streaming" | "done" | "error">("idle");
  const [lastPrompt, setLastPrompt] = useState("");
  const controllerRef = useRef<AbortController | null>(null);

  async function submit(message: string) {
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;
    setLastPrompt(message);
    setAnswer("");
    setCitations([]);
    setStatus("streaming");

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
        signal: controller.signal,
      });
      if (!response.ok || !response.body) throw new Error("Chat request failed");

      await parseNdjsonStream(response.body, (event) => {
        if (event.type === "token") setAnswer((current) => current + event.text);
        if (event.type === "citation") {
          setCitations((current) => [...current, event.citation]);
        }
        if (event.type === "error") setStatus("error");
        if (event.type === "done") setStatus("done");
      });
    } catch (error) {
      if (!(error instanceof DOMException && error.name === "AbortError")) {
        setStatus("error");
      }
    }
  }

  return (
    <div className="chat-shell">
      <ChatInput disabled={status === "streaming"} onSubmit={submit} />
      <StreamedAnswer answer={answer} citations={citations} status={status} />
      {status === "error" && lastPrompt ? (
        <button type="button" onClick={() => submit(lastPrompt)}>
          Retry
        </button>
      ) : null}
    </div>
  );
}
