import { Suspense } from "react";
import { ArchitectureSummary } from "@/components/architecture-summary";
import { ChatShell } from "@/components/chat-shell";

const samplePrompts = [
  "How should production agent changes be evaluated?",
  "When should authorization be applied in RAG retrieval?",
  "When would WebSockets be preferable to HTTP streaming?",
];

export default function Home() {
  return (
    <main className="page-shell">
      <header className="hero">
        <div className="hero-badge">Next.js 16 · FastAPI · LangGraph</div>
        <p className="eyebrow">Production-oriented AI systems portfolio</p>
        <h1>Enterprise AI Assistant</h1>
        <p className="hero-copy">
          A compact reference implementation for streamed, retrieval-grounded agent experiences
          with secure retrieval boundaries and regression evaluations.
        </p>
        <div className="capability-row" aria-label="Key capabilities">
          <span>Server Components</span>
          <span>HTTP streaming</span>
          <span>RAG + citations</span>
          <span>Eval-driven delivery</span>
        </div>
      </header>

      <section className="demo-grid">
        <div>
          <p className="section-label">Live demo</p>
          <h2>Ask the seeded knowledge base</h2>
          <ChatShell />
        </div>
        <aside className="prompt-card">
          <p className="section-label">Try these</p>
          <ul>
            {samplePrompts.map((prompt) => (
              <li key={prompt}>{prompt}</li>
            ))}
          </ul>
          <div className="privacy-note">
            <strong>Browser-safe citations only.</strong>
            <span>Raw chunks, ACL metadata and ranking scores stay server-side.</span>
          </div>
        </aside>
      </section>

      <Suspense fallback={<div className="architecture-card">Loading architecture notes…</div>}>
        <ArchitectureSummary />
      </Suspense>
    </main>
  );
}
