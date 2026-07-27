import React from 'react';
import { Target, TrendingUp, TrendingDown, Clock } from 'lucide-react';
import './SignalCenter.css';

export const SignalCenter: React.FC = () => {
  const signals = [
    { id: 1, symbol: 'EURUSD', action: 'BUY', confidence: 92, status: 'Active', time: '2m ago' },
    { id: 2, symbol: 'BTCUSD', action: 'SELL', confidence: 85, status: 'Waiting', time: '5m ago' },
    { id: 3, symbol: 'AAPL', action: 'BUY', confidence: 78, status: 'Active', time: '12m ago' },
  ];

  return (
    <div className="signal-center glass-panel">
      <div className="panel-header">
        <h3><Target size={18} /> Signal Center</h3>
      </div>
      <div className="signal-list">
        {signals.map((sig) => (
          <div key={sig.id} className="signal-card">
            <div className="signal-header">
              <span className="symbol">{sig.symbol}</span>
              <span className="time"><Clock size={12} /> {sig.time}</span>
            </div>
            <div className="signal-body">
              <div className={`action ${sig.action.toLowerCase()}`}>
                {sig.action === 'BUY' ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                {sig.action}
              </div>
              <div className="confidence">
                <div className="progress-bar">
                  <div className="progress" style={{ width: `${sig.confidence}%` }}></div>
                </div>
                <span>{sig.confidence}%</span>
              </div>
            </div>
            <div className="signal-footer">
              <span className={`status ${sig.status.toLowerCase()}`}>{sig.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
