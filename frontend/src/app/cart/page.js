export default function CartPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-white">
      <div className="max-w-2xl w-full p-8">
        <h1 className="text-2xl font-bold text-gray-900 text-center">Your Cart</h1>
        <div className="mt-6 rounded-xl border-2 border-purple-200 p-6 bg-gradient-to-br from-purple-50 via-pink-50 to-cyan-50">
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-lg bg-gradient-to-r from-amber-500 to-pink-500 text-white flex items-center justify-center text-2xl">🎈</div>
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <h2 className="font-semibold text-gray-900">Stealth Office Cushion (Whoopee Edition)</h2>
                <span className="text-sm font-bold text-gray-700">$19.99</span>
              </div>
              <p className="text-sm text-gray-600 mt-1">Comfort for the body, comedy for the soul. Disguised as a premium seat cushion.</p>
              <div className="mt-3 text-xs text-gray-500">Ships in 2-3 business days • Free returns within 30 days</div>
            </div>
          </div>
          <div className="mt-6 flex items-center justify-between">
            <span className="text-sm text-gray-700">Subtotal</span>
            <span className="text-sm font-bold text-gray-900">$19.99</span>
          </div>
          <button className="mt-6 w-full rounded-xl px-6 py-4 font-bold text-white shadow-lg bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500">Proceed to checkout</button>
        </div>
      </div>
    </div>
  );
}


