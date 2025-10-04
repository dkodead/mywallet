import React from 'react';
import NavBar from '@/components/NavBar';

export default function SettingsPage() {
  return (
    <>
      <NavBar />
      <main className="p-8">
        <h1 className="text-3xl font-bold mb-4">Settings</h1>
        <p className="text-gray-300 mb-4">
          Manage your preferences, connect or disconnect bank accounts, and configure
          notification settings here.  Authentication via Google can also be managed
          on this page.
        </p>
        <p className="text-gray-400">
          (Placeholder content — add forms and actions for user preferences.)
        </p>
      </main>
    </>
  );
}
