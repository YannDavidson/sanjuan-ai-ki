const exampleSources = [
  {
    source_id: "pr_gov_main",
    source_name: "PR.gov",
    trust_level: "official",
    url: "https://www.pr.gov/",
    snippet: "Central official portal of the Government of Puerto Rico.",
  },
  {
    source_id: "san_juan_municipio",
    source_name: "Municipio de San Juan",
    trust_level: "official",
    url: "https://sanjuan.pr/",
    snippet: "Municipal services, permits, announcements, and local San Juan information.",
  },
];

const exampleQuestions = [
  "How do I register a business in Puerto Rico?",
  "Where can I find San Juan municipal services?",
  "What official sources should I check for hurricane alerts?",
];

export default function AskPage() {
  return (
    <section className="container section">
      <div className="eyebrow">Ask SanJuan AI</div>
      <h1>Ask with sources, not guesses.</h1>
      <p className="lede">
        Retrieval is not connected yet, but this page is designed around the final citation-first answer experience:
        direct answer, confidence, citations, source cards, and safety notes when the topic is high-risk.
      </p>

      <div className="chat-shell section">
        <div className="card strong">
          <label htmlFor="question">
            <h3>Your question</h3>
          </label>
          <textarea
            id="question"
            placeholder="Ask about Puerto Rico services, San Juan resources, permits, tourism, weather, or business support..."
            defaultValue="Where do I start if I want to register a business in Puerto Rico?"
          />
          <div className="actions">
            <button className="button primary" type="button">
              Ask SanJuan AI
            </button>
            <span className="badge">Placeholder UI</span>
          </div>
        </div>

        <aside className="card">
          <h3>Example questions</h3>
          {exampleQuestions.map((question) => (
            <p key={question}>→ {question}</p>
          ))}
        </aside>
      </div>

      <div className="card strong">
        <div className="eyebrow">Planned response format</div>
        <div className="answer-box">
          <h2>SanJuan AI is not connected to retrieval yet.</h2>
          <p>
            The source registry is live, and the next implementation step is citation-based retrieval over trusted Puerto
            Rico sources. For high-risk topics like permits, taxes, health, legal, emergency, public benefits, courts,
            police, or immigration, SanJuan AI will require trusted official sources before giving a direct answer.
          </p>
          <div className="badge-row">
            <span className="badge">confidence: placeholder</span>
            <span className="badge">language: en</span>
            <span className="badge official">official sources prioritized</span>
          </div>
        </div>
      </div>

      <section className="section">
        <h2>Example source cards</h2>
        <div className="source-grid">
          {exampleSources.map((source) => (
            <article className="card" key={source.source_id}>
              <div className="badge-row">
                <span className="badge official">{source.trust_level}</span>
                <span className="badge">{source.source_id}</span>
              </div>
              <h3>{source.source_name}</h3>
              <p>{source.snippet}</p>
              <a className="button" href={source.url} target="_blank" rel="noreferrer">
                Open source
              </a>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
