import React from 'react';
import './Chart.css';

export const Chart: React.FC = () => {
  return (
    <div className="chart-wrapper">
      <div className="chart-header flex-between">
        <div className="chart-symbol-info">
          <h2>EURUSD</h2>
          <span className="chart-timeframe">15m</span>
        </div>
        <div className="chart-price-info">
          <span className="current-price">1.09245</span>
          <span className="price-change text-buy">+0.0012 (+0.11%)</span>
        </div>
      </div>
      
      <div className="chart-canvas-area">
        {/* Mocking a chart grid and ICT overlay */}
        <div className="mock-grid"></div>
        
        {/* Example ICT Overlays */}
        <div className="ict-fvg bg-buy" style={{ top: '30%', height: '40px' }}>
          <span>+FVG (Bullish)</span>
        </div>
        <div className="ict-ob bg-sell" style={{ top: '10%', height: '25px' }}>
          <span>-OB (Bearish)</span>
        </div>

        {/* Mock Price Line */}
        <svg className="mock-price-line" viewBox="0 0 100 100" preserveAspectRatio="none">
          <path d="M0,80 Q20,90 40,60 T70,40 T100,50" fill="none" stroke="var(--accent-blue)" strokeWidth="2" />
        </svg>
      </div>
    </div>
  );
};
