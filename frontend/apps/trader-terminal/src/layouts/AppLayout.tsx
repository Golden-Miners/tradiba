import React, { useEffect } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, Settings, Activity, Bell } from 'lucide-react';
import { NotificationCenter } from '@/components/notifications/NotificationCenter';
import { wsService } from '@/services/websocket';
import { useNotificationStore } from '@/store';
import './AppLayout.css';

export const AppLayout: React.FC = () => {
  const addNotification = useNotificationStore((state) => state.addNotification);

  useEffect(() => {
    wsService.connect();

    const handleSysAlert = (payload: any) => {
      addNotification({
        id: Math.random().toString(),
        title: payload.title || 'System Alert',
        message: payload.message || '',
        severity: payload.severity || 'info',
      });
    };

    wsService.subscribe('system_alert', handleSysAlert);

    return () => {
      wsService.unsubscribe('system_alert', handleSysAlert);
      wsService.disconnect();
    };
  }, [addNotification]);

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar glass-panel">
        <div className="sidebar-logo">
          <Activity size={28} color="var(--accent-primary)" />
          <h2>TRADIBA</h2>
        </div>
        <nav className="sidebar-nav">
          <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
            <LayoutDashboard size={20} />
            <span>Workspace</span>
          </NavLink>
          <NavLink to="/admin" className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}>
            <Settings size={20} />
            <span>Admin</span>
          </NavLink>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="topbar glass-panel">
          <div className="topbar-search">
            <input type="text" placeholder="Search symbol (e.g., XAUUSD)..." />
          </div>
          <div className="topbar-actions">
            <button className="icon-btn">
              <Bell size={20} />
            </button>
            <div className="user-avatar">AD</div>
          </div>
        </header>

        <div className="workspace-area">
          <Outlet />
        </div>
      </main>

      <NotificationCenter />
    </div>
  );
};
