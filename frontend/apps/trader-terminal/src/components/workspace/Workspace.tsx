import React from 'react';
import { Chart } from '../charts/Chart';
import { SignalPanel } from '../signals/SignalPanel';
import { OrderTicket } from '../orders/OrderTicket';
import { PortfolioDashboard } from '../portfolio/PortfolioDashboard';
import { AIInsightPanel } from '../research/AIInsightPanel';
import { AlertCenter } from '../alerts/AlertCenter';

import './Workspace.css';

export const Workspace: React.FC = () => {
  return (
    <div className="workspace-container">
      {/* Left Sidebar */}
      <aside className="workspace-sidebar">
        <div className="sidebar-header">
          <h2 className="brand-logo">Tradiba</h2>
          <span className="brand-version">v3.2</span>
        </div>
        <AlertCenter />
      </aside>

      {/* Main Center Area */}
      <main className="workspace-main">
        <section className="main-chart-area glass-panel">
          <Chart />
        </section>
        <section className="main-signals-area glass-panel">
          <SignalPanel />
        </section>
      </main>

      {/* Right Panel Area */}
      <aside className="workspace-right-panel">
        <section className="portfolio-area glass-panel">
          <PortfolioDashboard />
        </section>
        <section className="order-area glass-panel">
          <OrderTicket />
        </section>
        <section className="ai-insight-area glass-panel">
          <AIInsightPanel />
        </section>
      </aside>
    </div>
  );
};
