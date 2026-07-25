import { useEffect } from 'react';
import { wsManager } from '../websocket/WebSocketManager';
import { useAuthStore } from '../stores/authStore';

export const useWebSocket = () => {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);

  useEffect(() => {
    if (isAuthenticated) {
      wsManager.connect();
    } else {
      wsManager.disconnect();
    }

    return () => {
      wsManager.disconnect();
    };
  }, [isAuthenticated]);

  return wsManager;
};
