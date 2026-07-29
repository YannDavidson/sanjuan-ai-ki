import path from "node:path";

import type { NextConfig } from "next";

const repositoryRoot = path.resolve(process.cwd(), "../..");

const nextConfig: NextConfig = {
  output: "standalone",
  outputFileTracingRoot: repositoryRoot,
  outputFileTracingIncludes: {
    "/sources": ["../../data/sources/pr_sources.yml"],
  },
};

export default nextConfig;
