import { create } from 'zustand';

// --- Auth Store ---
interface AuthState {
  token: string | null;
  user: any | null;
  login: (token: string, user: any) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('tradiba_token'),
  user: null,
  login: (token, user) => {
    localStorage.setItem('tradiba_token', token);
    set({ token, user });
  },
  logout: () => {
    localStorage.removeItem('tradiba_token');
    set({ token: null, user: null });
  },
}));

// --- Market Data Store ---
interface MarketState {
  symbols: Record<string, any>; // Latest quotes
  updateSymbol: (symbol: string, data: any) => void;
}

export const useMarketStore = create<MarketState>((set) => ({
  symbols: {},
  updateSymbol: (symbol, data) =>
    set((state) => ({
      symbols: { ...state.symbols, [symbol]: data },
    })),
}));

// --- Notifications Store ---
interface Notification {
  id: string;
  title: string;
  message: string;
  severity: 'info' | 'warning' | 'critical' | 'emergency';
}

interface NotificationState {
  notifications: Notification[];
  addNotification: (n: Notification) => void;
  removeNotification: (id: string) => void;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],
  addNotification: (n) =>
    set((state) => ({ notifications: [n, ...state.notifications].slice(0, 50) })),
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
}));
