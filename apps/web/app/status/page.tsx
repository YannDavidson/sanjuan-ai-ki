import { formatLabel } from "@/lib/sources";
import { formatStatusLabel, getSourceStatusReport } from "@/lib/sourceStatus";

const STATUS_ORDER = ["healthy", "thin", "stale", "unknown_freshness", "empty", "failed", "missing"];

function StatusBadge({ value }: { value: string }) {
  const className = value === "healthy" ? "badge healthy" : value === "failed" || value === "missing" ? "badge danger" : "badge warning";
  return <span className={className}>{formatStatusLabel(value)}</span>;
}

export default function StatusPage() {
  const report = getSourceStatusReport();
  const sources = [...report.sources].sort((left, right) => {
    const leftIndex = STATUS_ORDER.indexOf(left.status);
    const rightIndex = STATUS_ORDER.indexOf(right.status);
    return (leftIndex === -1 ? 99 : leftIndex) - (rightIndex === -1 ? 99 : rightIndex) || left.name.localeCompare(right.name);
  });

  return (
    <section className="container section">
      <div className="eyebrow">Source Health</div>
      <h1>Freshness and status dashboard.</h1>
      <p className="lede">
        Track which Puerto Rico sources are healthy, stale, thin, missing, or broken before SanJuan AI trusts them for
        citation-backed answers.
      </p>

      {report.artifact_missing ? (
        <div className="notice">
          Generate the dashboard data with <code>python -m packages.ingestion.source_status --pretty --write-json</code> after
          running batch ingestion.
        </div>
      ) : null}

      <div className="metric-grid">
        <article className="metric-card">
          <span>Total sources</span>
          <strong>{report.total_sources}</strong>
        </article>
        {STATUS_ORDER.filter((status) => report.by_status[status]).map((status) => (
          <article className="metric-card" key={status}>
            <span>{formatStatusLabel(status)}</span>
            <strong>{report.by_status[status]}</strong>
          </article>
        ))}
      </div>

      {report.generated_at ? <p className="muted">Generated at {new Date(report.generated_at).toLocaleString()}</p> : null}

      <div className="status-table-wrap">
        <table className="status-table">
          <thead>
            <tr>
              <th>Source</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Category</th>
              <th>Trust</th>
              <th>Text</th>
              <th>Age</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((source) => (
              <tr key={source.source_id}>
                <td>
                  <a href={source.url} target="_blank" rel="noreferrer">
                    {source.name}
                  </a>
                  <small>{source.reason}</small>
                </td>
                <td>
                  <StatusBadge value={source.status} />
                </td>
                <td>{formatStatusLabel(source.priority)}</td>
                <td>{formatLabel(source.category)}</td>
                <td>{formatLabel(source.trust_level)}</td>
                <td>{source.text_length.toLocaleString()} chars</td>
                <td>{source.age_days === null || source.age_days === undefined ? "—" : `${source.age_days}d`}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
