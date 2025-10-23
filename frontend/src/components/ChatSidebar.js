"use client";

import Link from "next/link";

export default function ChatSidebar({ open, onClose, sendPrompt }) {
  return (
    <div
      className={`${open ? "translate-x-0" : "-translate-x-full"} fixed inset-y-0 left-0 z-50 w-72 bg-white shadow-2xl transform transition-transform duration-300 lg:translate-x-0 lg:static lg:inset-0`}
    >
      <div className="flex items-center justify-between p-6 border-b bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500">
        <div>
          <h1 className="font-black text-white text-lg">OfficeLifeline</h1>
          <p className="text-xs text-cyan-100 font-medium">Workplace Problems • Meet Solutions</p>
        </div>
        <button onClick={onClose} className="lg:hidden p-2 rounded-lg hover:bg-white/20 text-white">
          ✖
        </button>
      </div>

      <div className="p-6 space-y-6">
        <div>
          <h3 className="text-sm font-bold text-gray-800 mb-3">Quick Links</h3>
          <div className="space-y-2 text-sm text-gray-700">
            <a href="/kb" className="block p-3 rounded-lg border border-gray-200 hover:bg-gradient-to-r hover:from-cyan-50 hover:to-pink-50 hover:border-purple-300 transition">
              📚 Knowledge Base
            </a>
            <a href="/" className="block p-3 rounded-lg border border-gray-200 hover:bg-gradient-to-r hover:from-cyan-50 hover:to-pink-50 hover:border-purple-300 transition">
              🏠 Home
            </a>
            <a href="/cart" className="block p-3 rounded-lg border border-gray-200 hover:bg-gradient-to-r hover:from-cyan-50 hover:to-pink-50 hover:border-purple-300 transition">
              🛒 Cart
            </a>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-bold text-gray-800 mb-3">Try these prompts</h3>
          <div className="space-y-2">
            {[
              "Billing question about an invoice",
              "Technical issue: app throws an error",
              "Policy question about privacy",
            ].map((q) => (
              <button
                key={q}
                onClick={() => sendPrompt?.(q)}
                className="w-full text-left p-3 text-xs text-gray-600 hover:bg-gradient-to-r hover:from-cyan-50 hover:to-pink-50 rounded-lg transition border border-gray-200 hover:border-purple-300"
              >
                💬 {q}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}


