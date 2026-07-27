import React from 'react';
import './SignalPanel.css';

export const SignalPanel: React.FC = () => {
  const signals = [
    { id: 1, type: 'BUY', symbol: 'EURUSD', strategy: 'Silver Bullet', time: '10:00 AM', confidence: '92%' },
    { id: 2, type: 'SELL', symbol: 'GBPUSD', strategy: 'Judas Swing', time: '09:45 AM', confidence: '85%' },
    { id: 3, type: 'BUY', symbol: 'XAUUSD', strategy: 'Macro Sync', time: '08:30 AM', confidence: '78%' },
  ];

  return (
    <div className="signal-wrapper">
      <h3 className="panel-title">Active Signals</h3>
      
      <div className="signal-table">
        <div className="signal-header row">
          <span>Side</span>
          <span>Symbol</span>
          <span>Strategy</span>
          <span>Time</span>
          <span>Conf</span>
        </div>
        
        <div className="signal-body">
          {signals.map(s => (
            <div key={s.id} className="signal-row row">
              <span className={`signal-badge ${s.type === 'BUY' ? 'bg-buy' : 'bg-sell'}`}>
                {s.type}
              </span>
              <span className="font-bold">{s.symbol}</span>
              <span className="text-muted">{s.strategy}</span>
              <span className="text-muted">{s.time}</span>
              <span className="font-bold">{s.confidence}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
