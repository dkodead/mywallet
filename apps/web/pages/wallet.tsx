import React from 'react';
import NavBar from '@/components/NavBar';

export default function WalletPage() {
  return (
    <>
      <NavBar />
      <main className="p-8">
        <h1 className="text-3xl font-bold mb-4">Wallet Overview</h1>
        <p className="text-gray-300 mb-4">
          Here you'll see your account balances, recent transactions, spending
          analytics and budget projections.  Connect your bank via Plaid,
          TrueLayer or Tink to populate this page with live data.
        </p>
        <p className="text-gray-400">
          (Placeholder content — implement bank adapters and charts.)
        </p>
      </main>
    </>
  );
}
