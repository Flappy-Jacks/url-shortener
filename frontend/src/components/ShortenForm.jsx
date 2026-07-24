import { useState } from "react";
import { createLink } from "../api.js";

export default function ShortenForm({ onCreated }) {
  const [url, setUrl] = useState("");
  const [customCode, setCustomCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const link = await createLink(url, customCode);
      setUrl("");
      setCustomCode("");
      onCreated(link);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="shorten-form" onSubmit={handleSubmit}>
      <div className="field">
        <label htmlFor="url">Link to shorten</label>
        <input
          id="url"
          type="url"
          required
          placeholder="https://example.com/a/very/long/path"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
      </div>
      <div className="field field-inline">
        <label htmlFor="code">Custom code (optional)</label>
        <input
          id="code"
          type="text"
          placeholder="myproject"
          value={customCode}
          onChange={(e) => setCustomCode(e.target.value)}
        />
      </div>
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? "Shortening…" : "Shorten"}
      </button>
    </form>
  );
}
