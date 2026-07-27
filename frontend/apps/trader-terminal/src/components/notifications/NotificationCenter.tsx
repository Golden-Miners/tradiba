import React from 'react';
import { useNotificationStore } from '@/store';
import { X, AlertCircle, Info, AlertTriangle, XOctagon } from 'lucide-react';
import clsx from 'clsx';
import './NotificationCenter.css';

export const NotificationCenter: React.FC = () => {
  const { notifications, removeNotification } = useNotificationStore();

  if (notifications.length === 0) return null;

  return (
    <div className="notification-center">
      {notifications.map((notif) => {
        let Icon = Info;
        if (notif.severity === 'warning') Icon = AlertTriangle;
        if (notif.severity === 'critical') Icon = AlertCircle;
        if (notif.severity === 'emergency') Icon = XOctagon;

        return (
          <div key={notif.id} className={clsx('notification-toast', `severity-${notif.severity}`)}>
            <div className="toast-icon">
              <Icon size={20} />
            </div>
            <div className="toast-content">
              <h4>{notif.title}</h4>
              <p>{notif.message}</p>
            </div>
            <button onClick={() => removeNotification(notif.id)} className="toast-close">
              <X size={16} />
            </button>
          </div>
        );
      })}
    </div>
  );
};
