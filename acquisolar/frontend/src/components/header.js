// Header.js
import React from 'react';

const Header = () => {
  return (
    <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: '#98d2f2', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
      <h1>AcquiSolar</h1>
      <nav>
        <a href="/about" style={{ color: '#7cc2e7', textDecoration: 'none' }}>About Us</a>
      </nav>
    </header>
  );
};

export default Header;