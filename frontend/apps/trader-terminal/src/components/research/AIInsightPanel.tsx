import React from 'react';
import './AIInsightPanel.css';

export const AIInsightPanel: React.FC = () => {
  return (
    <div className="insight-wrapper">
      <div className="flex-between">
        <h3 className="panel-title">AI Market Narrative</h3>
        <div className="pulse-indicator"></div>
      </div>
      
      <div className="insight-content">
        <p className="narrative-text">
          Market is exhibiting a strong bullish divergence on the 1H timeframe. A Fair Value Gap (FVG) has been formed at <strong>1.09150</strong>.
        </p>
        
        <div className="evidence-list">
          <div className="evidence-item">
            <span className="dot bg-buy"></span>
            <span>DXY weakness detected across majors.</span>
          </div>
          <div className="evidence-item">
            <span className="dot bg-buy"></span>
            <span>Liquidity sweep confirmed below Asian session low.</span>
          </div>
        </div>

        <div className="confidence-score mt-auto">
          <span>Directional Bias: <strong>BULLISH</strong></span>
          <span className="score bg-buy">88%</span>
        </div>
      </div>
    </div>
  );
};
