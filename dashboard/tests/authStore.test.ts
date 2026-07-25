import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useAuthStore } from '../src/stores/authStore';
import * as jwtDecode from 'jwt-decode';

vi.mock('jwt-decode', () => ({
  jwtDecode: vi.fn(),
}));

describe('Auth Store', () => {
  beforeEach(() => {
    useAuthStore.setState({
      token: null,
      roles: [],
      username: null,
      isAuthenticated: false,
    });
    vi.clearAllMocks();
  });

  it('should login correctly with a valid token', () => {
    const mockToken = 'mock-valid-token';
    const mockPayload = { sub: 'admin', roles: ['Admin'], exp: 9999999999 };
    
    (jwtDecode.jwtDecode as any).mockReturnValue(mockPayload);

    useAuthStore.getState().login(mockToken);

    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(true);
    expect(state.token).toBe(mockToken);
    expect(state.roles).toEqual(['Admin']);
    expect(state.username).toBe('admin');
  });

  it('should logout correctly', () => {
    useAuthStore.setState({
      token: 'some-token',
      roles: ['Admin'],
      username: 'admin',
      isAuthenticated: true,
    });

    useAuthStore.getState().logout();

    const state = useAuthStore.getState();
    expect(state.isAuthenticated).toBe(false);
    expect(state.token).toBeNull();
    expect(state.roles).toEqual([]);
    expect(state.username).toBeNull();
  });
});
