import type { Citation } from "@/lib/chat-types";

export function Citations({ citations }: { citations: Citation[] }) {
  if (!citations.length) return null;
  return (
    <section aria-label="Sources" className="citations">
      <h3>Sources</h3>
      <ul>
        {citations.map((citation) => (
          <li key={citation.id}>
            <strong>{citation.title}</strong>
            {citation.section ? <span> — {citation.section}</span> : null}
            <p>{citation.snippet}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
