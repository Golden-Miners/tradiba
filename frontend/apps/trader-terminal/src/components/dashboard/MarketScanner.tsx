import React from 'react';
import { Filter, Activity, Zap } from 'lucide-react';
import './MarketScanner.css';

export const MarketScanner: React.FC = () => {
  const assets = [
    { symbol: 'XAUUSD', type: 'Forex', pattern: 'CHOCH', volatility: 'High', aiScore: 94 },
    { symbol: 'BTCUSD', type: 'Crypto', pattern: 'FVG', volatility: 'High', aiScore: 88 },
    { symbol: 'US30', type: 'Indices', pattern: 'Liquidity Sweep', volatility: 'Medium', aiScore: 72 },
    { symbol: 'XAUUSD', type: 'Metals', pattern: 'Order Block', volatility: 'Low', aiScore: 65 },
  ];

  return (
    <div className="market-scanner glass-panel">
      <div className="panel-header">
        <h3><Activity size={18} /> Market Scanner</h3>
        <button className="icon-btn"><Filter size={16} /></button>
      </div>

      <div className="scanner-filters">
        <span className="badge active">All</span>
        <span className="badge">Forex</span>
        <span className="badge">Crypto</span>
        <span className="badge">Indices</span>
      </div>

      <div className="scanner-list">
        {assets.map((asset) => (
          <div key={asset.symbol} className="scanner-card">
            <div className="scanner-main">
              <span className="symbol">{asset.symbol}</span>
              <span className="type">{asset.type}</span>
            </div>
            <div className="scanner-details">
              <span className="pattern">{asset.pattern}</span>
              <span className={`volatility ${asset.volatility.toLowerCase()}`}>
                {asset.volatility} Vol
              </span>
            </div>
            <div className="scanner-score">
              <Zap size={14} color="var(--accent-primary)" />
              <span className="score">{asset.aiScore}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
