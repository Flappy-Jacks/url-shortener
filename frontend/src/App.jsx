import { useEffect, useState } from "react";
import ShortenForm from "./components/ShortenForm.jsx";
import LinkList from "./components/LinkList.jsx";
import { listLinks } from "./api.js";

export default function App() {
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(true);

  function refresh() {
    listLinks()
      .then(setLinks)
      .finally(() => setLoading(false));
  }

  useEffect(refresh, []);

  function handleCreated(newLink) {
    setLinks((prev) => [newLink, ...prev]);
  }

  return (
    <div className="page">
      <header>
        <h1>snip</h1>
        <p className="tagline">Turn long links into short, trackable ones.</p>
      </header>

      <ShortenForm onCreated={handleCreated} />

      <section>
        <h2>Your links</h2>
        {loading ? <p className="empty">Loading…</p> : <LinkList links={links} />}
      </section>
    </div>
  );
}
