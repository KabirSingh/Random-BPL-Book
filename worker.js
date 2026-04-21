const UPSTREAM = "https://gateway.bibliocommons.com/v2/libraries/bpl";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin":  "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default {
  async fetch(request) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url      = new URL(request.url);
    const upstream = new URL(UPSTREAM + url.pathname + url.search);

    const response = await fetch(upstream.toString(), {
      headers: { "User-Agent": "Mozilla/5.0" },
    });

    const body    = await response.text();
    const headers = new Headers(CORS_HEADERS);
    headers.set("Content-Type", response.headers.get("Content-Type") || "application/json");

    return new Response(body, { status: response.status, headers });
  },
};
