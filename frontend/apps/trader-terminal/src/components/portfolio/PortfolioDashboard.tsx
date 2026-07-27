import React from 'react';
import './PortfolioDashboard.css';

export const PortfolioDashboard: React.FC = () => {
  return (
    <div className="portfolio-wrapper">
      <h3 className="panel-title">Portfolio</h3>
      
      <div className="portfolio-metric-large">
        <span className="metric-label">Total Equity</span>
        <div className="metric-value">$1,245,670.00</div>
      </div>

      <div className="portfolio-stats-grid">
        <div className="stat-box">
          <span className="stat-label">Daily P&L</span>
          <span className="stat-val text-buy">+$12,450 (1.0%)</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Free Margin</span>
          <span className="stat-val">$890,200</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Open Pos</span>
          <span className="stat-val">4</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Drawdown</span>
          <span className="stat-val text-sell">-2.4%</span>
        </div>
      </div>
    </div>
  );
};
