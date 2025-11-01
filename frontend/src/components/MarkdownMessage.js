"use client";

// Minimal markdown renderer for bold and bullet lists
// - Converts **bold** to <strong>
// - Converts leading "- " to <li> within <ul>
export default function MarkdownMessage({ text }) {
  if (!text) return null;

  // Normalize jammed lists like "steps:1. ...2. ..." → insert newlines before 1. / 2. / 3.
  let normalized = String(text)
    // newline before digit-dot sequences if they follow non-newline
    .replace(/([^\n])(\d+\.\s)/g, (m, p1, p2) => `${p1}\n${p2}`)
    // newline after colons before a numbered list
    .replace(/:\s*(\d+\.\s)/g, (m, p1) => `:\n${p1}`);

  const paragraphs = normalized.split(/\n\n+/);

  return (
    <div className="space-y-3">
      {paragraphs.map((para, idx) => {
        const lines = para.split(/\n/);
        const isBullet = lines.every((l) => /^\s*-\s+/.test(l));
        const isOrdered = lines.every((l) => /^\s*\d+\.\s+/.test(l));
        if (isBullet) {
          return (
            <ul key={idx} className="list-disc pl-6 space-y-1">
              {lines.map((l, i) => (
                <li key={i}>{renderInline(l.replace(/^\s*-\s+/, ""))}</li>
              ))}
            </ul>
          );
        }
        if (isOrdered) {
          return (
            <ol key={idx} className="list-decimal pl-6 space-y-1">
              {lines.map((l, i) => (
                <li key={i}>{renderInline(l.replace(/^\s*\d+\.\s+/, ""))}</li>
              ))}
            </ol>
          );
        }
        return (
          <p key={idx} className="text-sm leading-relaxed whitespace-pre-wrap">
            {renderInline(para)}
          </p>
        );
      })}
    </div>
  );
}

function renderInline(s) {
  const parts = s.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) => {
    const m = part.match(/^\*\*([^*]+)\*\*$/);
    if (m) return <strong key={i}>{m[1]}</strong>;
    return <span key={i}>{part}</span>;
  });
}
