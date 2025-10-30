import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, RotateCcw, Menu, X, HelpCircle, Settings, Briefcase, Zap, Coffee } from 'lucide-react';

export default function ChatbotFrontend() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      content: "Welcome to OfficeLifeline! 🏢 Where we solve workplace problems with a healthy dose of sarcasm and questionable life choices! I'm your AI support specialist, and fair warning: I come with a built-in dad joke dispenser and zero corporate filter! How can I help you navigate the beautiful chaos of office life today?",
      sender: 'ai',
      timestamp: new Date().toLocaleTimeString(),
      agentType: 'support'
    }
  ]);
  
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  const [currentSuggestion, setCurrentSuggestion] = useState(0);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Rotate suggestion every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSuggestion(prev => (prev + 1) % suggestionQuestions.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMessage]);

  // Dad jokes database
  const dadJokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What do you call a fake noodle? An impasta!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "What do you call a bear with no teeth? A gummy bear!",
    "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!",
    "Why don't programmers like nature? It has too many bugs!"
  ];

  // Office-themed satirical responses
  const satiricalResponses = [
    "Ah yes, another classic case of 'have you tried being passionate about meaningless corporate objectives?' Let me check our database of soul-crushing solutions...",
    "I see you're experiencing what we call 'acute workplace reality syndrome.' Symptoms include existential dread and an uncontrollable urge to update your LinkedIn profile. Let me help...",
    "Welcome to the wonderful world of office politics, where logic goes to die and common sense is considered a radical concept! Let me translate this into corporate-speak for you...",
    "Ah, the age-old problem of trying to be productive while drowning in meetings about meetings. Have you considered the ancient art of 'looking busy while actually being busy?'",
    "I detect traces of 'why-is-this-my-life-itis' in your query. Don't worry, it's highly contagious in office environments. Let me prescribe some actual solutions...",
    "Another victim of the 'urgent but not important' task epidemic! Fear not, I have non-corporate-approved methods to help you reclaim your sanity..."
  ];

  // Mock function to simulate routing and responses
  const sendMessage = async (message) => {
    if (!message.trim()) return;
    
    const userMessage = {
      id: Date.now(),
      content: message,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setStreamingMessage('');

    // Determine response type - SIMPLIFIED!
    const triggerDadJoke = message.toLowerCase().includes('joke') || 
                          message.toLowerCase().includes('funny') ||
                          message.toLowerCase().includes('dad joke');

    let responseText = '';
    let agentType = 'support';

    if (triggerDadJoke) {
      // Pure dad joke response - much simpler!
      const randomJoke = dadJokes[Math.floor(Math.random() * dadJokes.length)];
      responseText = `🚨 EMOTIONAL SUPPORT DAD JOKE ACTIVATED! 🚨\n\n${randomJoke}\n\nThere! Feeling better? That's what I'm here for! 😄`;
      agentType = 'dad-joke';
    } else {
      // Regular professional support
      responseText = getSeriousResponse(message);
    }

    // Simulate streaming effect
    for (let i = 0; i <= responseText.length; i++) {
      setStreamingMessage(responseText.substring(0, i));
      await new Promise(resolve => setTimeout(resolve, 25));
    }

    const aiResponse = {
      id: Date.now() + 1,
      content: responseText,
      sender: 'ai',
      timestamp: new Date().toLocaleTimeString(),
      agentType: agentType
    };

    setMessages(prev => [...prev, aiResponse]);
    setStreamingMessage('');
    setIsLoading(false);
  };

  const getSeriousResponse = (message) => {
    // Generate appropriate responses based on message content
    if (message.toLowerCase().includes('meeting') || message.toLowerCase().includes('schedule')) {
      return "For meeting management, I recommend time-blocking techniques and setting clear agendas with defined outcomes. Consider implementing the 'no agenda, no meeting' rule and always question if this could be an email instead.";
    } else if (message.toLowerCase().includes('boss') || message.toLowerCase().includes('manager')) {
      return "Managing up can be challenging. Focus on clear communication, document decisions, and try to understand their priorities. Schedule regular check-ins and always come with solutions, not just problems.";
    } else if (message.toLowerCase().includes('deadline') || message.toLowerCase().includes('stress') || message.toLowerCase().includes('overwhelm')) {
      return "For deadline stress, try breaking large tasks into smaller chunks, prioritize ruthlessly using methods like Eisenhower Matrix, and don't be afraid to communicate realistic timelines early and often.";
    } else if (message.toLowerCase().includes('coworker') || message.toLowerCase().includes('colleague') || message.toLowerCase().includes('team')) {
      return "Workplace relationships require diplomacy and clear boundaries. Focus on collaborative solutions, document important decisions, and remember that you can't control others' behavior - only your response to it.";
    } else if (message.toLowerCase().includes('productivity') || message.toLowerCase().includes('focus')) {
      return "For better focus, try techniques like the Pomodoro method, eliminate notification distractions during deep work, and create physical or digital boundaries between different types of tasks.";
    } else {
      return "I understand your workplace concern. The key is often finding the balance between what the company needs and what actually works in practice. Let me help you navigate this with some concrete strategies.";
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };

  const clearChat = () => {
    setMessages([{
      id: 1,
      content: "Welcome to OfficeLifeline! 🏢 Where we solve workplace problems with a healthy dose of sarcasm and questionable life choices! I'm your AI support specialist, and fair warning: I come with a built-in dad joke dispenser and zero corporate filter! How can I help you navigate the beautiful chaos of office life today?",
      sender: 'ai',
      timestamp: new Date().toLocaleTimeString(),
      agentType: 'support'
    }]);
  };

  const getAgentInfo = (agentType) => {
    const agents = {
      support: { name: 'Workplace Specialist', color: 'bg-gradient-to-r from-cyan-500 to-blue-500', icon: '🏢', badge: 'SUPPORT' },
      'dad-joke': { name: 'ESDJ Bot', color: 'bg-gradient-to-r from-pink-500 to-rose-500', icon: '🤣', badge: 'DAD JOKE' }
    };
    return agents[agentType] || agents.support;
  };

  const suggestionQuestions = [
    "Help with my workload",
    "Tell me a dad joke",
    "Meeting overload help",
    "Deadline stress advice"
  ];

  const companyMottos = [
    "Turning workplace drama into workplace dharma! 🧘‍♀️",
    "We put the 'fun' in 'fundamentally broken corporate systems'! 🎉",
    "Because every office needs a reality check and a dad joke! ⚡",
    "Solving problems one eye-roll at a time! 👀"
  ];

  return (
    <div className="h-screen bg-gradient-to-br from-cyan-50 via-pink-50 to-purple-50 flex">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} fixed inset-y-0 left-0 z-50 w-80 bg-white shadow-2xl transform transition-transform duration-300 lg:translate-x-0 lg:static lg:inset-0`}>
        <div className="flex items-center justify-between p-6 border-b bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-lg">
              <Briefcase className="w-7 h-7 text-cyan-600" />
            </div>
            <div>
              <h1 className="font-black text-white text-xl">OfficeLifeline</h1>
              <p className="text-xs text-cyan-100 font-medium">Workplace Problems • Meet Solutions</p>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-2 rounded-lg hover:bg-white/20 text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="p-6">
          <div className="mb-6">
            <h3 className="text-sm font-bold text-gray-800 mb-3 flex items-center gap-2">
              <Zap className="w-4 h-4 text-purple-500" />
              Today's Office Wisdom
            </h3>
            <div className="p-4 bg-gradient-to-r from-cyan-100 via-purple-100 to-pink-100 rounded-xl border-l-4 border-cyan-500">
              <p className="text-sm text-gray-700 font-medium">
                {companyMottos[Math.floor(Math.random() * companyMottos.length)]}
              </p>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-sm font-bold text-gray-800 mb-3">Quick Escape Routes</h3>
            <div className="space-y-2">
              <button
                onClick={clearChat}
                className="w-full flex items-center gap-3 p-3 text-sm text-gray-700 hover:bg-gradient-to-r hover:from-cyan-50 hover:to-purple-50 rounded-lg transition border-2 border-cyan-200 hover:border-purple-300"
              >
                <RotateCcw className="w-4 h-4" />
                Fresh Start Support Session
              </button>
              <button className="w-full flex items-center gap-3 p-3 text-sm text-gray-700 hover:bg-gradient-to-r hover:from-pink-50 hover:to-purple-50 rounded-lg transition border-2 border-pink-200 hover:border-purple-300">
                <HelpCircle className="w-4 h-4" />
                Office Survival Guide
              </button>
              <button className="w-full flex items-center gap-3 p-3 text-sm text-gray-700 hover:bg-gradient-to-r hover:from-purple-50 hover:to-cyan-50 rounded-lg transition border-2 border-purple-200 hover:border-cyan-300">
                <Settings className="w-4 h-4" />
                Reality Check Settings
              </button>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-sm font-bold text-gray-800 mb-3">Try These Office Dilemmas!</h3>
            <div className="space-y-2">
              {suggestionQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => sendMessage(question)}
                  className="w-full text-left p-3 text-xs text-gray-600 hover:bg-gradient-to-r hover:from-cyan-50 hover:to-pink-50 rounded-lg transition border border-gray-200 hover:border-purple-300"
                  disabled={isLoading}
                >
                  💼 "{question}"
                </button>
              ))}
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-100 via-pink-100 to-cyan-100 p-4 rounded-xl border-2 border-purple-200">
            <h4 className="font-bold text-sm text-gray-800 mb-2 flex items-center gap-1">
              <span className="text-lg">🤖</span> AI Personalities On Duty
            </h4>
            <div className="space-y-2 text-xs text-gray-600">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 bg-cyan-500 rounded-full"></span>
                <span>Workplace Specialist (Professional)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                <span>Office Reality Check (Satirical)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 bg-pink-500 rounded-full"></span>
                <span>ESDJ Bot (Pure Dad Jokes)</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b-2 border-purple-200 shadow-lg p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-lg hover:bg-purple-100"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <div className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse" style={{animationDelay: '0.5s'}}></div>
                <div className="w-2 h-2 bg-pink-500 rounded-full animate-pulse" style={{animationDelay: '1s'}}></div>
              </div>
              <span className="font-bold text-gray-900 text-lg">OfficeLifeline Support</span>
              <span className="text-sm text-purple-600 bg-purple-100 px-3 py-1 rounded-full font-semibold">Multi-Agent Active</span>
            </div>
          </div>
          <div className="text-sm text-gray-500 flex items-center gap-2">
            <Coffee className="w-4 h-4" />
            Powered by LangGraph & FastAPI
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${
                message.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.sender === 'ai' && (
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-12 h-12 rounded-2xl ${getAgentInfo(message.agentType).color} flex items-center justify-center text-white shadow-lg text-xl`}>
                    {getAgentInfo(message.agentType).icon}
                  </div>
                  <div className={`text-xs px-2 py-1 rounded-full font-bold text-white shadow-sm ${
                    message.agentType === 'dad-joke' 
                      ? 'bg-gradient-to-r from-pink-500 to-rose-500 animate-pulse'
                      : 'bg-gradient-to-r from-cyan-500 to-blue-500'
                  }`}>
                    {getAgentInfo(message.agentType).badge}
                  </div>
                </div>
              )}
              
              <div className={`max-w-xs lg:max-w-md px-5 py-4 rounded-2xl shadow-md ${
                message.sender === 'user'
                  ? 'bg-gradient-to-r from-gray-600 to-gray-700 text-white'
                  : message.agentType === 'dad-joke'
                    ? 'bg-gradient-to-r from-pink-100 to-rose-100 border-2 border-pink-300 text-gray-900'
                    : 'bg-white border-2 border-cyan-200 text-gray-900'
              }`}>
                <p className="text-sm leading-relaxed whitespace-pre-line">{message.content}</p>
                <p className={`text-xs mt-3 ${
                  message.sender === 'user' ? 'text-gray-300' : 'text-gray-500'
                }`}>
                  {message.timestamp}
                </p>
              </div>

              {message.sender === 'user' && (
                <div className="w-12 h-12 bg-gradient-to-r from-gray-400 to-gray-600 rounded-2xl flex items-center justify-center shadow-lg">
                  <User className="w-6 h-6 text-white" />
                </div>
              )}
            </div>
          ))}

          {/* Streaming message */}
          {streamingMessage && (
            <div className="flex gap-3 justify-start">
              <div className="flex flex-col items-center gap-1">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center text-white animate-pulse shadow-lg text-xl">
                  🤖
                </div>
                <div className="text-xs px-2 py-1 rounded-full font-bold text-white bg-gradient-to-r from-purple-500 to-pink-500">
                  THINKING...
                </div>
              </div>
              <div className="max-w-xs lg:max-w-md px-5 py-4 rounded-2xl bg-white border-2 border-cyan-200 text-gray-900 shadow-md">
                <p className="text-sm whitespace-pre-line">{streamingMessage}<span className="animate-pulse">|</span></p>
              </div>
            </div>
          )}

          {/* Loading indicator */}
          {isLoading && !streamingMessage && (
            <div className="flex gap-3 justify-start">
              <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-2xl flex items-center justify-center shadow-lg">
                <Loader2 className="w-6 h-6 text-white animate-spin" />
              </div>
              <div className="max-w-xs lg:max-w-md px-5 py-4 rounded-2xl bg-white border-2 border-purple-200 shadow-md">
                <p className="text-sm text-gray-600">Consulting the office wisdom database...</p>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Single Rotating Suggestion (when minimal messages) */}
        {messages.length <= 1 && (
          <div className="px-4 pb-4">
            <div className="text-center">
              <div className="max-w-sm mx-auto">
                <div className="p-4 text-sm text-gray-600 bg-gradient-to-r from-cyan-50 via-purple-50 to-pink-50 rounded-xl border-2 border-purple-200 shadow-sm">
                  <span className="text-purple-500 font-semibold">💡 Try asking: </span>
                  <span className="italic">"{suggestionQuestions[currentSuggestion]}"</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="bg-white border-t-2 border-purple-200 p-4 shadow-lg">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-3">
              <input
                ref={inputRef}
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="What's your office crisis today? 🏢 (Type 'dad joke' for emergency humor!)"
                disabled={isLoading}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                className="flex-1 p-4 border-2 border-purple-300 rounded-xl focus:ring-4 focus:ring-cyan-200 focus:border-cyan-400 disabled:bg-gray-100 placeholder-gray-500 text-gray-900"
              />
              <button
                onClick={handleSubmit}
                disabled={isLoading || !inputMessage.trim()}
                className="px-6 py-4 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 text-white rounded-xl hover:from-cyan-600 hover:via-purple-600 hover:to-pink-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition shadow-lg hover:shadow-xl flex items-center gap-2 font-bold"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
            <div className="mt-3 text-xs text-gray-500 text-center">
              💼 Press Enter to submit • Our AI agents might roast your workplace or drop dad jokes! 🤣
            </div>
          </div>
        </div>
      </div>

      {/* Mobile backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}