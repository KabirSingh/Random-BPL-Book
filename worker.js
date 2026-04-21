const ALLOWED_HOSTS = new Set([
  "gateway.bibliocommons.com",
  "sdws02.sirsidynix.net",
  "detp.ent.sirsi.net",
]);

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

    const url       = new URL(request.url);
    const parts     = url.pathname.split("/").filter(Boolean);
    const host      = parts[0];
    const remainder = "/" + parts.slice(1).join("/");

    if (!ALLOWED_HOSTS.has(host)) {
      return new Response("Not allowed", { status: 403 });
    }

    const upstream = `https://${host}${remainder}${url.search}`;

    const response = await fetch(upstream, {
      headers: { "User-Agent": "Mozilla/5.0" },
    });

    const body    = await response.text();
    const headers = new Headers(CORS_HEADERS);
    headers.set("Content-Type", response.headers.get("Content-Type") || "application/json");

    return new Response(body, { status: response.status, headers });
  },
};
