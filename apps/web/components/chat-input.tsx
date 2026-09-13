import type { FormEvent } from "react";
import { useState } from "react";

export function ChatInput({
  disabled,
  onSubmit,
}: {
  disabled: boolean;
  onSubmit: (message: string) => Promise<void>;
}) {
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = message.trim();
    if (!value || disabled) return;
    setMessage("");
    await onSubmit(value);
  }

  return (
    <form onSubmit={submit} className="chat-form">
      <label htmlFor="message">Ask the enterprise AI assistant</label>
      <textarea
        id="message"
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        rows={3}
        placeholder="How should production agent changes be evaluated?"
      />
      <button type="submit" disabled={disabled || !message.trim()}>
        {disabled ? "Streaming…" : "Send"}
      </button>
    </form>
  );
}
