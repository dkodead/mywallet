import React from 'react';

const NavBar: React.FC = () => {
  return (
    <nav className="w-full bg-navy-700 p-4 flex items-center justify-between">
      <div className="text-xl font-bold text-white">wallet.dkoded.io</div>
      <ul className="flex space-x-4">
        <li><a href="/today" className="text-gray-300 hover:text-white">Today</a></li>
        <li><a href="/news" className="text-gray-300 hover:text-white">News</a></li>
        <li><a href="/wallet" className="text-gray-300 hover:text-white">Wallet</a></li>
        <li><a href="/settings" className="text-gray-300 hover:text-white">Settings</a></li>
      </ul>
    </nav>
  );
};

export default NavBar;
