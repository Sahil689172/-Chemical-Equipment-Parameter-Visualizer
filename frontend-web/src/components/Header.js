import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="app-header">
      <div className="header-left">
        <div className="logo">
          <div className="logo-icon">⚗️</div>
          <div className="logo-text">
            <div className="logo-title">ChemViz Engineer Portal</div>
          </div>
        </div>
      </div>
      
      <div className="header-center">
        <h1 className="main-title">Parameter Visualizer</h1>
        <p className="subtitle">Real-time analysis of equipment datasets</p>
      </div>
      
      <div className="header-right">
        <div className="status-indicator">
          <span className="status-icon">✓</span>
          <span className="status-text">SYSTEM ONLINE</span>
        </div>
      </div>
    </header>
  );
}

export default Header;
