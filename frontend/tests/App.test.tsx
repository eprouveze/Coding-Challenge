import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

test('renders heading', () => {
  render(<App />);
  expect(screen.getByText(/Event Management/i)).toBeInTheDocument();
});
