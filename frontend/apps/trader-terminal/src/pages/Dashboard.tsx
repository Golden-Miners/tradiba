import React from 'react';
import { Chart } from '@/components/charts/Chart';
import { SignalCenter } from '@/components/trading/SignalCenter';
import { OrderTicket } from '@/components/trading/OrderTicket';
import { PortfolioDashboard } from '@/components/portfolio/PortfolioDashboard';
import { MarketScanner } from '@/components/dashboard/MarketScanner';
import { AICopilot } from '@/components/ai/AICopilot';
import './Dashboard.css';

export const Dashboard: React.FC = () => {
  return (
    <div className="dashboard-grid">
      <div className="grid-area-chart">
        <Chart symbol="EURUSD" />
      </div>
      <div className="grid-area-scanner">
        <MarketScanner />
      </div>
      <div className="grid-area-signals">
        <SignalCenter />
      </div>
      <div className="grid-area-order">
        <OrderTicket />
      </div>
      <div className="grid-area-portfolio">
        <PortfolioDashboard />
      </div>
      <div className="grid-area-ai">
        <AICopilot />
      </div>
    </div>
  );
};
