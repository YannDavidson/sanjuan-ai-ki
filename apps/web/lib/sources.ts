import fs from "node:fs";
import path from "node:path";

import yaml from "js-yaml";

export type Source = {
  id: string;
  name: string;
  url: string;
  category: string;
  geography: string;
  language: string;
  trust_level: string;
  source_type: string;
  update_frequency?: string;
  notes?: string;
};

type SourceRegistry = {
  sources?: Source[];
};

function candidateRegistryPaths(): string[] {
  return [
    path.join(process.cwd(), "data", "sources", "pr_sources.yml"),
    path.join(process.cwd(), "..", "..", "data", "sources", "pr_sources.yml"),
    path.join(__dirname, "..", "..", "..", "..", "data", "sources", "pr_sources.yml"),
  ];
}

export function getSources(): Source[] {
  const sourcePath = candidateRegistryPaths().find((candidate) => fs.existsSync(candidate));
  if (!sourcePath) {
    console.warn("SanJuan AI source registry was not included in this build.");
    return [];
  }

  try {
    const file = fs.readFileSync(sourcePath, "utf8");
    const registry = yaml.load(file) as SourceRegistry;
    return registry.sources ?? [];
  } catch (error) {
    console.error("Could not load SanJuan AI source registry.", error);
    return [];
  }
}

export function uniqueValues(sources: Source[], key: keyof Source): string[] {
  return Array.from(new Set(sources.map((source) => String(source[key] ?? "")).filter(Boolean))).sort();
}

export function formatLabel(value: string): string {
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}
