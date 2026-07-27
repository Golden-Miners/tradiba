import React from 'react';
import './OrderTicket.css';

export const OrderTicket: React.FC = () => {
  return (
    <div className="order-ticket-wrapper">
      <h3 className="panel-title">Order Ticket</h3>
      
      <div className="order-form">
        <div className="form-group">
          <label>Symbol</label>
          <input type="text" value="EURUSD" readOnly className="input-field symbol-input" />
        </div>
        
        <div className="form-group">
          <label>Risk (%)</label>
          <input type="range" min="0.1" max="5" step="0.1" defaultValue="1.0" className="risk-slider" />
          <div className="risk-value">1.0% ($12,456)</div>
        </div>

        <div className="order-actions">
          <button className="btn-buy">
            <span>BUY MARKET</span>
            <span className="action-price">1.09245</span>
          </button>
          <button className="btn-sell">
            <span>SELL MARKET</span>
            <span className="action-price">1.09242</span>
          </button>
        </div>
      </div>
    </div>
  );
};
