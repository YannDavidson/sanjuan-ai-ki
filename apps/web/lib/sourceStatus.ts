import fs from "node:fs";
import path from "node:path";

import { getSources } from "@/lib/sources";

export type SourceStatus = {
  source_id: string;
  name: string;
  url: string;
  category: string;
  geography: string;
  language: string;
  trust_level: string;
  source_type: string;
  status: string;
  reason: string;
  priority: string;
  status_code?: number | null;
  content_length?: number | null;
  text_length: number;
  fetched_at?: string | null;
  age_days?: number | null;
  content_hash?: string | null;
  raw_path?: string | null;
  error?: string | null;
};

export type SourceStatusReport = {
  generated_at?: string;
  total_sources: number;
  by_status: Record<string, number>;
  by_priority: Record<string, number>;
  sources: SourceStatus[];
  artifact_missing?: boolean;
};

function buildFallbackReport(): SourceStatusReport {
  const sources = getSources();
  return {
    total_sources: sources.length,
    by_status: { missing: sources.length },
    by_priority: {},
    artifact_missing: true,
    sources: sources.map((source) => ({
      source_id: source.id,
      name: source.name,
      url: source.url,
      category: source.category,
      geography: source.geography,
      language: source.language,
      trust_level: source.trust_level,
      source_type: source.source_type,
      status: "missing",
      reason: "No source status artifact has been generated yet.",
      priority: source.trust_level === "official" ? "high" : "normal",
      text_length: 0,
    })),
  };
}

export function getSourceStatusReport(): SourceStatusReport {
  const statusPath = path.join(process.cwd(), "..", "..", "data", "status", "source_status.json");
  if (!fs.existsSync(statusPath)) {
    return buildFallbackReport();
  }

  const file = fs.readFileSync(statusPath, "utf8");
  return JSON.parse(file) as SourceStatusReport;
}

export function formatStatusLabel(value: string): string {
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}
