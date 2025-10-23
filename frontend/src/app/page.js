export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-cyan-50 via-pink-50 to-purple-50">
      <main className="flex w-full max-w-xl flex-col items-center gap-8 p-8">
        <div className="text-center">
          <h1 className="text-3xl font-black text-gray-900">OfficeLifeline</h1>
          <p className="mt-2 text-sm text-gray-600">Workplace Problems • Meet Solutions</p>
        </div>
        <a
          href="/chat"
          className="inline-flex items-center justify-center rounded-xl px-8 py-4 font-bold text-white shadow-lg transition-transform hover:scale-[1.02] focus:outline-none focus:ring-4 focus:ring-cyan-200 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500"
        >
          Chat now
        </a>
      </main>
    </div>
  );
}
