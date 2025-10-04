import React from 'react';
import NavBar from '@/components/NavBar';

export default function Today() {
  return (
    <>
      <NavBar />
      <main className="p-8">
        <h1 className="text-3xl font-bold mb-4">Today's Dashboard</h1>
        <p className="text-gray-300 mb-4">
          This page will display your account balances and the top news stories from each
          category for the last 24 hours.  In a full deployment this page would call
          the `/news/daily` and `/banks/balances` endpoints and render the results.
        </p>
        <p className="text-gray-400">
          (Placeholder content — implement data fetching with React Query and display
          charts using Tremor.)
        </p>
      </main>
    </>
  );
}
