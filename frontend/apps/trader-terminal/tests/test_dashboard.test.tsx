import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { MarketScanner } from '../src/components/dashboard/MarketScanner';

describe('MarketScanner Component', () => {
  it('renders correctly', () => {
    render(<MarketScanner />);
    
    // Check if the component renders the header
    expect(screen.getByText('Market Scanner')).toBeDefined();
    
    // Check if it renders the scanner assets
    expect(screen.getByText('EURUSD')).toBeDefined();
    expect(screen.getByText('BTCUSD')).toBeDefined();
  });
});
