import React from 'react';
import NavBar from '@/components/NavBar';

export default function NewsPage() {
  return (
    <>
      <NavBar />
      <main className="p-8">
        <h1 className="text-3xl font-bold mb-4">News Intelligence</h1>
        <p className="text-gray-300 mb-4">
          This page will provide a deeper dive into the news topics across all categories,
          including cluster summaries, importance scores, and time filters.  Breaking
          news will also appear here as it happens.
        </p>
        <p className="text-gray-400">
          (Placeholder content — integrate with the `/news/daily` and `/news/breaking` API
          endpoints and render interactive components.)
        </p>
      </main>
    </>
  );
}
