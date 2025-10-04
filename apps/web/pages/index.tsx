import React from 'react';
import NavBar from '@/components/NavBar';

export default function Home() {
  return (
    <>
      <NavBar />
      <main className="p-8">
        <h1 className="text-3xl font-bold mb-4">Welcome to wallet.dkoded.io</h1>
        <p className="text-lg text-gray-300">
          Your unified dashboard for personal finance and curated news.  Use the navigation
          above to explore today's highlights, deep dives into the news, your wallet
          overview and application settings.
        </p>
      </main>
    </>
  );
}
