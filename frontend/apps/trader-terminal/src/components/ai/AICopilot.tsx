import React from 'react';
import { Bot, HelpCircle, MessageSquare, Activity, TrendingUp } from 'lucide-react';
import './AICopilot.css';

export const AICopilot: React.FC = () => {
  return (
    <div className="ai-copilot glass-panel">
      <div className="panel-header ai-header">
        <h3><Bot size={18} /> AI Copilot</h3>
        <span className="ai-status online">Online</span>
      </div>

      <div className="chat-container">
        <div className="chat-message ai">
          <div className="avatar"><Bot size={16} /></div>
          <div className="message-bubble">
            <p>I detected a <strong>BOS</strong> (Break of Structure) on EURUSD 5m. The current Order Block suggests strong support at 1.0850. Would you like me to explain the setup or calculate risk for a long entry?</p>
            <div className="evidence-link">
              <Activity size={12} /> View Decision Intelligence Evidence
            </div>
          </div>
        </div>

        <div className="chat-suggestions">
          <button><HelpCircle size={14} /> Explain Setup</button>
          <button><TrendingUp size={14} /> Calculate Risk</button>
          <button><MessageSquare size={14} /> Market Summary</button>
        </div>
      </div>

      <div className="chat-input-area">
        <input type="text" placeholder="Ask AI Copilot about the market..." />
        <button className="send-btn"><Bot size={16} /></button>
      </div>
    </div>
  );
};
