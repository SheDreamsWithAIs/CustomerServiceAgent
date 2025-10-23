export default function AgentBadge({ color, icon, badge }) {
  return (
    <div className="flex flex-col items-center gap-1">
      <div className={`w-12 h-12 rounded-2xl bg-gradient-to-r ${color} flex items-center justify-center text-white shadow-lg text-xl`}>
        {icon}
      </div>
      <div className="text-xs px-2 py-1 rounded-full font-bold text-white shadow-sm bg-gradient-to-r from-gray-800 to-gray-600">
        {badge}
      </div>
    </div>
  );
}


