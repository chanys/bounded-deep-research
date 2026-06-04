import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Emit a static site (an `out/` folder), so the frontend can be hosted on S3 +
  // CloudFront with no Node server at runtime. The API is FastAPI, reached from the
  // browser via NEXT_PUBLIC_API_BASE, so no Next.js server features are needed.
  output: "export",
};

export default nextConfig;
