import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { jwtDecode } from 'jwt-decode';

interface AuthState {
  token: string | null;
  roles: string[];
  username: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

interface JwtPayload {
  sub: string;
  roles: string[];
  exp: number;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      roles: [],
      username: null,
      isAuthenticated: false,
      login: (token: string) => {
        try {
          const decoded = jwtDecode<JwtPayload>(token);
          set({
            token,
            roles: decoded.roles || [],
            username: decoded.sub,
            isAuthenticated: true,
          });
        } catch (e) {
          console.error("Invalid token", e);
        }
      },
      logout: () => set({ token: null, roles: [], username: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
