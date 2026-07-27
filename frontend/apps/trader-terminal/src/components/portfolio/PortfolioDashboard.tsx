import React from 'react';
import { PieChart, Briefcase, TrendingUp } from 'lucide-react';
import './PortfolioDashboard.css';

export const PortfolioDashboard: React.FC = () => {
  return (
    <div className="portfolio-dashboard glass-panel">
      <div className="panel-header">
        <h3><Briefcase size={18} /> Portfolio</h3>
      </div>
      
      <div className="portfolio-content">
        <div className="equity-summary">
          <div className="balance-label">Total Equity</div>
          <div className="balance-value">$1,245,678.90</div>
          <div className="balance-change positive">
            <TrendingUp size={16} /> +$12,450 (1.01%) Today
          </div>
        </div>

        <div className="metrics-grid">
          <div className="metric">
            <span className="label">Open P&L</span>
            <span className="value positive">+$3,210.50</span>
          </div>
          <div className="metric">
            <span className="label">Margin Used</span>
            <span className="value">15.4%</span>
          </div>
          <div className="metric">
            <span className="label">Max Drawdown</span>
            <span className="value negative">-4.2%</span>
          </div>
          <div className="metric">
            <span className="label">Win Rate</span>
            <span className="value">68%</span>
          </div>
        </div>

        <div className="allocation">
          <h4><PieChart size={14} /> Asset Allocation</h4>
          <div className="allocation-bar">
            <div className="alloc fx" style={{ width: '45%' }}></div>
            <div className="alloc crypto" style={{ width: '30%' }}></div>
            <div className="alloc indices" style={{ width: '25%' }}></div>
          </div>
          <div className="allocation-legend">
            <span><span className="dot fx"></span> Forex (45%)</span>
            <span><span className="dot crypto"></span> Crypto (30%)</span>
            <span><span className="dot indices"></span> Indices (25%)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
