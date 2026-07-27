import React from 'react';
import { Users, Shield, Server, Activity } from 'lucide-react';
import './AdminConsole.css';

export const AdminConsole: React.FC = () => {
  return (
    <div className="admin-console">
      <div className="admin-header glass-panel">
        <h2>Admin Console</h2>
        <p>Manage users, roles, and platform settings.</p>
      </div>

      <div className="admin-grid">
        <div className="admin-card glass-panel">
          <div className="card-icon"><Users size={24} /></div>
          <h3>User Management</h3>
          <p>Manage 1,245 active traders and researchers.</p>
          <button className="admin-action">Manage Users</button>
        </div>
        
        <div className="admin-card glass-panel">
          <div className="card-icon"><Shield size={24} /></div>
          <h3>Roles & Permissions</h3>
          <p>Configure RBAC and access policies.</p>
          <button className="admin-action">Configure RBAC</button>
        </div>

        <div className="admin-card glass-panel">
          <div className="card-icon"><Server size={24} /></div>
          <h3>Broker Integration</h3>
          <p>Manage MT5 and other broker connections.</p>
          <button className="admin-action">Manage Brokers</button>
        </div>

        <div className="admin-card glass-panel">
          <div className="card-icon"><Activity size={24} /></div>
          <h3>System Audit</h3>
          <p>View platform event and security logs.</p>
          <button className="admin-action">View Logs</button>
        </div>
      </div>
    </div>
  );
};
