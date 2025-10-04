// A simple navigation bar component using Tailwind CSS and shadcn/ui conventions.
//
// This component is a placeholder and does not depend on any external libraries.
// Replace with shadcn/ui components when running in an environment with
// next-auth and proper dependencies installed.

import React from 'react';

export const NavBar: React.FC = () => {
  return (
    <nav className="w-full bg-navy-800 text-white p-4 flex items-center justify-between">
      <div className="text-xl font-bold">wallet.dkoded.io</div>
      <ul className="flex space-x-4">
        <li><a href="/today" className="hover:underline">Today</a></li>
        <li><a href="/news" className="hover:underline">News</a></li>
        <li><a href="/wallet" className="hover:underline">Wallet</a></li>
        <li><a href="/settings" className="hover:underline">Settings</a></li>
      </ul>
    </nav>
  );
};

export default NavBar;
