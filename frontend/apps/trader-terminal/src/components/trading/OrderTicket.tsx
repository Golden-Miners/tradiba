import React, { useState } from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import './OrderTicket.css';

export const OrderTicket: React.FC = () => {
  const [orderType, setOrderType] = useState('MARKET');
  const [side, setSide] = useState<'BUY' | 'SELL'>('BUY');

  return (
    <div className="order-ticket glass-panel">
      <div className="panel-header">
        <h3>Order Ticket</h3>
      </div>
      
      <div className="ticket-content">
        <div className="side-selector">
          <button 
            className={`btn-side buy ${side === 'BUY' ? 'active' : ''}`}
            onClick={() => setSide('BUY')}
          >
            BUY
          </button>
          <button 
            className={`btn-side sell ${side === 'SELL' ? 'active' : ''}`}
            onClick={() => setSide('SELL')}
          >
            SELL
          </button>
        </div>

        <div className="type-selector">
          {['MARKET', 'LIMIT', 'STOP'].map(type => (
            <button 
              key={type}
              className={`btn-type ${orderType === type ? 'active' : ''}`}
              onClick={() => setOrderType(type)}
            >
              {type}
            </button>
          ))}
        </div>

        <div className="input-group">
          <label>Quantity</label>
          <input type="number" defaultValue={1} step={0.1} />
        </div>

        {orderType !== 'MARKET' && (
          <div className="input-group">
            <label>Price</label>
            <input type="number" placeholder="Enter price" />
          </div>
        )}

        <div className="brackets">
          <div className="input-group">
            <label>Take Profit</label>
            <input type="number" placeholder="Optional" />
          </div>
          <div className="input-group">
            <label>Stop Loss</label>
            <input type="number" placeholder="Optional" />
          </div>
        </div>

        <button className={`btn-submit ${side.toLowerCase()}`}>
          {side === 'BUY' ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
          Place {side} Order
        </button>
      </div>
    </div>
  );
};
