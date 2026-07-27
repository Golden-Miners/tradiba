import React from 'react';
import './AlertCenter.css';

export const AlertCenter: React.FC = () => {
  const alerts = [
    { id: 1, type: 'critical', message: 'NFP Data Release in 5m', time: 'Just now' },
    { id: 2, type: 'info', message: 'XAUUSD reached target +1R', time: '12m ago' },
    { id: 3, type: 'warning', message: 'Spread widening on XAUUSD', time: '45m ago' },
  ];

  return (
    <div className="alert-center-wrapper">
      <h3 className="sidebar-heading">System Alerts</h3>
      <div className="alert-list">
        {alerts.map(a => (
          <div key={a.id} className={`alert-item alert-${a.type}`}>
            <span className="alert-dot"></span>
            <div className="alert-content">
              <p className="alert-msg">{a.message}</p>
              <span className="alert-time">{a.time}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="sidebar-menu-links mt-auto">
        <button className="menu-link active">Terminal</button>
        <button className="menu-link">Backtesting</button>
        <button className="menu-link">Journal</button>
        <button className="menu-link">Settings</button>
      </div>
    </div>
  );
};
