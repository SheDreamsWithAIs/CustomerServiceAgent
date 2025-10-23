export default function MessageBubble({ sender, variant, timestamp, children }) {
  const classes =
    sender === "user"
      ? "bg-gradient-to-r from-gray-600 to-gray-700 text-white"
      : variant === "esdj"
      ? "bg-gradient-to-r from-amber-50 to-pink-50 border-2 border-amber-200 text-gray-900"
      : "bg-white border-2 border-cyan-200 text-gray-900";

  return (
    <div className={`max-w-xs lg:max-w-md px-5 py-4 rounded-2xl shadow-md ${classes}`}>
      <p className="text-sm leading-relaxed whitespace-pre-line">{children}</p>
      {timestamp ? (
        <p className={`text-xs mt-3 ${sender === "user" ? "text-gray-300" : "text-gray-500"}`}>{timestamp}</p>
      ) : null}
    </div>
  );
}


