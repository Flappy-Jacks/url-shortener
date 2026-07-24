const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function handle(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

export function createLink(originalUrl, customCode) {
  return fetch(`${API_BASE}/api/links`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      original_url: originalUrl,
      custom_code: customCode || null,
    }),
  }).then(handle);
}

export function listLinks() {
  return fetch(`${API_BASE}/api/links`).then(handle);
}

export const shortUrlFor = (code) => `${API_BASE}/${code}`;
