import { create } from 'zustand';

export interface Position {
  symbol: string;
  ticket: number;
  volume: number;
  price_open: number;
  current_price: number;
  profit: number;
  type: string;
}

interface PortfolioState {
  equity: number;
  balance: number;
  free_margin: number;
  positions_count: number;
  active_positions: Position[];
  updatePortfolio: (data: Partial<PortfolioState>) => void;
  updatePositions: (positions: Position[]) => void;
}

export const usePortfolioStore = create<PortfolioState>((set) => ({
  equity: 0,
  balance: 0,
  free_margin: 0,
  positions_count: 0,
  active_positions: [],
  updatePortfolio: (data) => set((state) => ({ ...state, ...data })),
  updatePositions: (positions) => set({ active_positions: positions }),
}));
