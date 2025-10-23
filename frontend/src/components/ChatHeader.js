"use client";

export default function ChatHeader({ onOpenSidebar }) {
  return (
    <div className="bg-white border-b-2 border-purple-200 shadow-lg p-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button onClick={onOpenSidebar} className="lg:hidden p-2 rounded-lg hover:bg-purple-100">
          ☰
        </button>
        <span className="font-bold text-gray-900 text-lg">OfficeLifeline Support</span>
        <span className="text-sm text-purple-600 bg-purple-100 px-3 py-1 rounded-full font-semibold">Ready to Assist</span>
      </div>
      <div className="text-sm text-gray-500">Powered by AI ✨</div>
    </div>
  );
}


