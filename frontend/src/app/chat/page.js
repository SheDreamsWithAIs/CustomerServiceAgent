"use client";

import { useEffect, useRef, useState } from "react";
import ChatHeader from "@/components/ChatHeader";
import ChatSidebar from "@/components/ChatSidebar";
import { chat as apiChat, chatStream } from "@/lib/api";

// Visible personas (UI): brand assistant (default) and ESDJ (dad jokes)
const AGENTS = {
  brand: { name: "OfficeLifeline Assistant", badge: "ASSISTANT", color: "from-cyan-500 to-purple-500", icon: "🏢" },
  esdj: { name: "ESDJ Bot", badge: "DAD JOKE", color: "from-amber-500 to-pink-500", icon: "🤣" },
};

// Under-the-hood routing types: billing, technical, policy, esdj, orchestrator
function chooseAgentFor(message) {
  const text = message.toLowerCase();
  if (/(dad\s*joke|joke|funny)/.test(text)) return "esdj";
  if (/(bill|invoice|pricing|charge|payment)/.test(text)) return "billing";
  if (/(error|bug|issue|technical|setup|install)/.test(text)) return "technical";
  if (/(policy|privacy|terms|compliance|security)/.test(text)) return "policy";
  return "orchestrator";
}

function getDisplayAgentType(agentType) {
  return agentType === "esdj" ? "esdj" : "brand";
}

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      content:
        "Welcome to OfficeLifeline! Ask anything about billing, technical issues, or policies and I’ll route it to the right specialist.",
      sender: "ai",
      timestamp: "",
      agentType: "brand",
    },
  ]);

  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState("");
  const [streamingAgentType, setStreamingAgentType] = useState("brand");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [threadId, setThreadId] = useState(() => `web_${Date.now()}`);
  const userId = "user_123"; // simple default for personalization

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingMessage]);

  function formatAssistantText(text, route) {
    if (!text) return text;
    let t = text;
    // Insert newlines before Markdown bullets like "- **Field**" when jammed together
    t = t.replace(/:\s*-\s+\*\*/g, ":\n- **");
    t = t.replace(/\)\s*-\s+\*\*/g, ")\n- **");
    t = t.replace(/([^\n])-\s+\*\*/g, (m, p1) => `${p1}\n- **`);
    // Compact excessive blank lines
    t = t.replace(/\n{3,}/g, "\n\n");
    return t.trim();
  }

  async function sendMessage(message) {
    if (!message.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      content: message,
      sender: "user",
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);
    setStreamingMessage("");

    // Show a short placeholder while awaiting backend
    setStreamingAgentType("brand");
    setStreamingMessage("Working on it…");

    try {
      // Stream tokens first for better UX
      let streamed = "";
      await chatStream({
        message,
        userId,
        threadId,
        onChunk: (ch) => {
          streamed += ch;
          setStreamingMessage(streamed);
        },
      });

      // Fetch structured details after stream completes
      const res = await apiChat({ message, userId, threadId });
      let responseText = streamed || res?.message || "";

      // Append a concise summary for billing only (avoid duplicates)
      if (res?.route === "billing" && res?.billing) {
        const b = res.billing;
        const alreadyHasSummary = /Plan:\s|Balance\s|User ID:|Email:/.test(responseText);
        if (!alreadyHasSummary) {
          const parts = [];
          if (b.plan) parts.push(`Plan ${b.plan}`);
          if (b.balance_due != null && b.currency) parts.push(`Balance ${b.balance_due} ${b.currency}`);
          if (b.last_invoice_id) parts.push(`Invoice ${b.last_invoice_id}`);
          if (parts.length) responseText += `\n\n${parts.join(" • ")}`;
        }
      }

      const agentFromRoute = res?.route || "orchestrator";
      const aiResponse = {
        id: Date.now() + 1,
        content: formatAssistantText(responseText, res?.route),
        sender: "ai",
        timestamp: new Date().toLocaleTimeString(),
        agentType: agentFromRoute === "tech_support" ? "technical" : agentFromRoute,
      };

      setMessages((prev) => [...prev, aiResponse]);
    } catch (err) {
      const aiResponse = {
        id: Date.now() + 1,
        content: `Error: ${err?.message || "Request failed"}`,
        sender: "ai",
        timestamp: new Date().toLocaleTimeString(),
        agentType: "brand",
      };
      setMessages((prev) => [...prev, aiResponse]);
    } finally {
      setStreamingMessage("");
      setIsLoading(false);
    }
  }

  function startNewChat() {
    setIsLoading(false);
    setStreamingMessage("");
    setStreamingAgentType("brand");
    setInputMessage("");
    setThreadId(`web_${Date.now()}`);
    setMessages([
      {
        id: Date.now(),
        content:
          "Welcome to OfficeLifeline! Ask anything about billing, technical issues, or policies and I’ll route it to the right specialist.",
        sender: "ai",
        timestamp: "",
        agentType: "brand",
      },
    ]);
  }

  function AgentBadge({ agentType }) {
    const agent = AGENTS[agentType] ?? AGENTS.brand;
    return (
      <div className="flex flex-col items-center gap-1">
        <div
          className={`w-12 h-12 rounded-2xl bg-gradient-to-r ${agent.color} flex items-center justify-center text-white shadow-lg text-xl`}
        >
          {agent.icon}
        </div>
        <div className="text-xs px-2 py-1 rounded-full font-bold text-white shadow-sm bg-gradient-to-r from-gray-800 to-gray-600">
          {agent.badge}
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-gradient-to-br from-cyan-50 via-pink-50 to-purple-50 flex">
      {/* Sidebar */}
      <ChatSidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} sendPrompt={(q) => sendMessage(q)} />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <ChatHeader onOpenSidebar={() => setSidebarOpen(true)} />

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => {
            const displayType = getDisplayAgentType(message.agentType);
            return (
              <div key={message.id} className={`flex gap-3 ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
                {message.sender === "ai" && <AgentBadge agentType={displayType} />}
              <div
                className={`max-w-xs lg:max-w-md px-5 py-4 rounded-2xl shadow-md ${
                  message.sender === "user"
                    ? "bg-gradient-to-r from-gray-600 to-gray-700 text-white"
                    : displayType === "esdj"
                    ? "bg-gradient-to-r from-amber-50 to-pink-50 border-2 border-amber-200 text-gray-900"
                    : "bg-white border-2 border-cyan-200 text-gray-900"
                }`}
              >
                <p className="text-sm leading-relaxed whitespace-pre-line">{message.content}</p>
                {message.timestamp ? (
                  <p className={`text-xs mt-3 ${message.sender === "user" ? "text-gray-300" : "text-gray-500"}`}>{message.timestamp}</p>
                ) : null}
              </div>
            </div>
            );
          })}

          {/* Streaming message */}
          {streamingMessage && (
            <div className="flex gap-3 justify-start">
              <AgentBadge agentType={streamingAgentType} />
              <div className="max-w-xs lg:max-w-md px-5 py-4 rounded-2xl bg-white border-2 border-cyan-200 text-gray-900 shadow-md">
                <p className="text-sm whitespace-pre-line">
                  {streamingMessage}
                  <span className="animate-pulse">|</span>
                </p>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t-2 border-purple-200 p-4 shadow-lg">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask about billing, technical issues, or policies..."
                disabled={isLoading}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage(inputMessage);
                  }
                }}
                className="flex-1 p-4 border-2 border-purple-300 rounded-xl focus:ring-4 focus:ring-cyan-200 focus:border-cyan-400 disabled:bg-gray-100 placeholder-gray-500 text-gray-900"
              />
              <button
                onClick={() => sendMessage(inputMessage)}
                disabled={isLoading || !inputMessage.trim()}
                className="px-6 py-4 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 text-white rounded-xl hover:from-cyan-600 hover:via-purple-600 hover:to-pink-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition shadow-lg hover:shadow-xl font-bold"
              >
                {isLoading ? "Thinking…" : "Send"}
              </button>
              <button
                onClick={startNewChat}
                disabled={isLoading}
                className="px-4 py-4 bg-white border-2 border-gray-300 text-gray-800 rounded-xl hover:bg-gray-50 transition shadow-sm font-semibold"
              >
                New Chat
              </button>
            </div>
            <div className="mt-3 text-xs text-gray-500 text-center">Press Enter to submit • Connected to backend API</div>
          </div>
        </div>
      </div>
    </div>
  );
}


