"use client";

// Minimal markdown renderer for bold and bullet lists
// - Converts **bold** to <strong>
// - Converts leading "- " to <li> within <ul>
export default function MarkdownMessage({ text }) {
  if (!text) return null;

  const paragraphs = String(text).split(/\n\n+/);

  return (
    <div className="space-y-3">
      {paragraphs.map((para, idx) => {
        const lines = para.split(/\n/);
        const isList = lines.every((l) => /^\s*-\s+/.test(l));
        if (isList) {
          return (
            <ul key={idx} className="list-disc pl-6 space-y-1">
              {lines.map((l, i) => (
                <li key={i}>{renderInline(l.replace(/^\s*-\s+/, ""))}</li>
              ))}
            </ul>
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
