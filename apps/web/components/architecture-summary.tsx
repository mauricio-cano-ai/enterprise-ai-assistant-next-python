export async function ArchitectureSummary() {
  await Promise.resolve();
  return (
    <section className="architecture-card">
      <div>
        <p className="section-label">Architecture</p>
        <h2>Deliberate boundaries, not a monolith</h2>
      </div>
      <ul className="architecture-grid">
        <li>
          <strong>Next.js App Router</strong>
          <span>Server-first shell with a small interactive chat boundary.</span>
        </li>
        <li>
          <strong>Streaming BFF</strong>
          <span>Route Handler forwards NDJSON without buffering the full answer.</span>
        </li>
        <li>
          <strong>FastAPI + LangGraph</strong>
          <span>Python owns retrieval, orchestration, grounding and stream events.</span>
        </li>
        <li>
          <strong>Evaluation gate</strong>
          <span>Golden cases protect citations, refusals and authorization behavior.</span>
        </li>
      </ul>
    </section>
  );
}
