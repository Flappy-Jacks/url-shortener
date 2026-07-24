import { shortUrlFor } from "../api.js";

export default function LinkList({ links }) {
  if (links.length === 0) {
    return <p className="empty">No links yet — shorten your first one above.</p>;
  }

  return (
    <table className="link-list">
      <thead>
        <tr>
          <th>Short link</th>
          <th>Destination</th>
          <th>Clicks</th>
        </tr>
      </thead>
      <tbody>
        {links.map((link) => {
          const short = shortUrlFor(link.code);
          return (
            <tr key={link.code}>
              <td>
                <a href={short} target="_blank" rel="noreferrer">
                  {short}
                </a>
                <button
                  className="copy-btn"
                  onClick={() => navigator.clipboard.writeText(short)}
                  title="Copy to clipboard"
                >
                  Copy
                </button>
              </td>
              <td className="destination">{link.original_url}</td>
              <td className="clicks">{link.click_count}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
