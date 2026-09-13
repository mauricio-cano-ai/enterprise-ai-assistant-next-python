import type { Citation } from "@/lib/chat-types";
import { Citations } from "./citations";

export function StreamedAnswer({
  answer,
  citations,
  status,
}: {
  answer: string;
  citations: Citation[];
  status: "idle" | "streaming" | "done" | "error";
}) {
  return (
    <section aria-live="polite" className="answer-card">
      <p>{answer || (status === "streaming" ? "Thinking…" : "Ask a question to begin.")}</p>
      <Citations citations={citations} />
    </section>
  );
}
