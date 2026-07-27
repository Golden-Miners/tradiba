import React from 'react';
import { Beaker, BarChart2, GitPullRequest } from 'lucide-react';
import './ResearchWorkspace.css';

export const ResearchWorkspace: React.FC = () => {
  return (
    <div className="research-workspace">
      <div className="research-header glass-panel">
        <h2><Beaker size={24} /> Research Workspace</h2>
        <p>Backtest experiments, strategy rankings, and feature importance analysis.</p>
      </div>

      <div className="research-content glass-panel">
        <div className="research-tabs">
          <button className="active"><GitPullRequest size={16} /> Experiments</button>
          <button><BarChart2 size={16} /> Walk-forward Analysis</button>
        </div>

        <div className="experiment-list">
          <div className="experiment-row header">
            <span>Experiment Name</span>
            <span>Strategy</span>
            <span>Sharpe</span>
            <span>Max DD</span>
            <span>Status</span>
          </div>
          <div className="experiment-row">
            <span>EXP-2026-1</span>
            <span>ICT Silver Bullet</span>
            <span className="positive">2.14</span>
            <span className="negative">-4.2%</span>
            <span className="badge success">Completed</span>
          </div>
          <div className="experiment-row">
            <span>EXP-2026-2</span>
            <span>Mean Reversion v2</span>
            <span className="positive">1.88</span>
            <span className="negative">-6.1%</span>
            <span className="badge success">Completed</span>
          </div>
          <div className="experiment-row">
            <span>EXP-2026-3</span>
            <span>ML Momentum Filter</span>
            <span>--</span>
            <span>--</span>
            <span className="badge running">Running...</span>
          </div>
        </div>
      </div>
    </div>
  );
};
