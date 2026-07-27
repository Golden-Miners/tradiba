import React from 'react';
import { Target, TrendingUp, TrendingDown, Clock } from 'lucide-react';
import './SignalCenter.css';

interface Signal {
  id: number;
  symbol: string;
  action: string;
  confidence: number;
  status: string;
  time: string;
  entry: string;
  sl: string;
  tp: string;
}

export const SignalCenter: React.FC = () => {
  const [signals, setSignals] = React.useState<Signal[]>([]);

  React.useEffect(() => {
    const fetchSignals = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/market/signals');
        const data = await res.json();
        if (Array.isArray(data)) {
          setSignals(data);
        }
      } catch (err) {
        console.error('Failed to fetch live signals', err);
      }
    };
    
    fetchSignals();
    const interval = setInterval(fetchSignals, 10000);
    return () => clearInterval(interval);
  }, []);

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
            <div className="signal-levels">
              <div className="level-item">
                <span className="level-label">Entry</span>
                <span className="level-value">{sig.entry}</span>
              </div>
              <div className="level-item sl">
                <span className="level-label">SL</span>
                <span className="level-value">{sig.sl}</span>
              </div>
              <div className="level-item tp">
                <span className="level-label">TP</span>
                <span className="level-value">{sig.tp}</span>
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
