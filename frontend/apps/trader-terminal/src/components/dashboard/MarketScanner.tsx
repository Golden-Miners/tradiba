import React, { useEffect, useState } from 'react';
import { Filter, Activity, Zap } from 'lucide-react';
import './MarketScanner.css';

interface Asset {
  symbol: string;
  type: string;
  price?: number;
  pattern: string;
  volatility: string;
  aiScore: number;
}

export const MarketScanner: React.FC = () => {
  const [assets, setAssets] = useState<Asset[]>([
    { symbol: 'XAUUSD', type: 'Metals', pattern: 'CHOCH', volatility: 'High', aiScore: 94 },
    { symbol: 'BTCUSD', type: 'Crypto', pattern: 'FVG', volatility: 'High', aiScore: 88 },
    { symbol: 'US30', type: 'Indices', pattern: 'Liquidity Sweep', volatility: 'Medium', aiScore: 72 },
    { symbol: 'EURUSD', type: 'Forex', pattern: 'Order Block', volatility: 'Low', aiScore: 65 },
  ]);

  useEffect(() => {
    const fetchTicks = async () => {
      try {
        const symbols = assets.map(a => a.symbol).join(',');
        const res = await fetch(`http://localhost:8000/api/market/ticks?symbols=${symbols}`);
        const data = await res.json();
        
        setAssets(prev => prev.map(a => {
          if (data[a.symbol]) {
            return { ...a, price: data[a.symbol].price };
          }
          return a;
        }));
      } catch (err) {
        console.error('Failed to fetch live ticks for scanner', err);
      }
    };

    fetchTicks();
    const interval = setInterval(fetchTicks, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="market-scanner glass-panel">
      <div className="panel-header">
        <h3><Activity size={18} /> Market Scanner (Live)</h3>
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
              <span className="pattern">{asset.price ? `$${asset.price.toFixed(2)}` : 'Loading...'}</span>
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
