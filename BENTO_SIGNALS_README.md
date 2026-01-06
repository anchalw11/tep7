# Bento Signals UI Component

A modern, glassmorphism-inspired signals display component built with React, TypeScript, and Tailwind CSS.

## Features

### 🎨 **Modern UI Design**
- **Glassmorphism**: Semi-transparent cards with backdrop blur effects
- **Bento Grid Layout**: Responsive grid with varying card sizes
- **Dark Theme**: Optimized for dark mode with subtle gradients
- **Interactive Elements**: Hover effects and smooth transitions

### 📊 **Smart Calculations**
- **Lot Size Calculation**: Automatically calculates recommended lot sizes based on:
  - Account equity
  - Risk per trade percentage
  - Stop loss distance
  - Maximum position limits

- **P&L Projections**: Real-time calculation of potential profits and losses:
  - Entry to take profit potential
  - Entry to stop loss risk
  - Position sizing impact

### 📈 **Signal Information Display**
- **Currency Pair**: EURUSD, GBPUSD, etc.
- **Direction**: BUY/SELL/LONG/SHORT with color-coded icons
- **Confidence Level**: Percentage with star ratings
- **Entry/Exit Levels**: Precise price points
- **Risk/Reward Ratio**: Calculated ratios
- **Status**: Active, Won, Lost, Pending states
- **Milestone**: Signal progression tracking

### 🔧 **Interactive Features**
- **Time Period Filtering**: 7d, 30d, 90d, 1y filters (when integrated)
- **Status Indicators**: Visual status with appropriate icons
- **Action Buttons**: Quick access to calculations and journal
- **Responsive Design**: Works on all screen sizes

## Component Structure

### `BentoGrid` (Base Component)
```tsx
import { BentoGrid } from './components/ui/bento-grid';

<BentoGrid items={signalItems} />
```

### `BentoSignals` (Signals Wrapper)
```tsx
import { BentoSignals } from './components/ui/bento-signals';

<BentoSignals
  signals={signalData}
  userEquity={10000}
  riskPerTrade={1}
/>
```

## Data Structure

### Signal Data Interface
```typescript
interface SignalData {
  pair: string;              // "EURUSD"
  direction: 'BUY' | 'SELL' | 'LONG' | 'SHORT';
  confidence: number;        // 50 (percentage)
  entryPrice: number;        // 1.085
  stopLoss: number;          // 1.083
  takeProfit: number;        // 1.087
  riskReward: string;        // "1:1.00"
  milestone: string;         // "M1"
  status: 'Won' | 'Lost' | 'Active' | 'Pending';
  timestamp: string;         // "1:40:23 PM"
  previousStatus?: 'Won' | 'Lost' | 'BE';
}
```

## Calculations

### Lot Size Formula
```typescript
// Risk amount = Account Equity × Risk Per Trade %
riskAmount = userEquity * (riskPerTrade / 100);

// Pip difference between entry and stop loss
pipDifference = Math.abs(entryPrice - stopLoss);

// Lot size = Risk Amount ÷ (Pip Difference × $10 per pip)
lotSize = riskAmount / (pipDifference * 10);

// Constrained between 0.01 and 10 lots
finalLotSize = Math.max(0.01, Math.min(lotSize, 10));
```

### P&L Calculation
```typescript
// For BUY/LONG positions
profitPips = takeProfit - entryPrice;
lossPips = entryPrice - stopLoss;

// For SELL/SHORT positions
profitPips = entryPrice - takeProfit;
lossPips = stopLoss - entryPrice;

// Final P&L = Pips × $10 per pip × Lot Size
potentialProfit = profitPips * 10 * lotSize;
potentialLoss = lossPips * 10 * lotSize;
```

## Usage Example

```tsx
import { BentoSignals, SignalData } from './components/ui/bento-signals';

const signals: SignalData[] = [
  {
    pair: "EURUSD",
    direction: "LONG",
    confidence: 50,
    entryPrice: 1.085,
    stopLoss: 1.083,
    takeProfit: 1.087,
    riskReward: "1:1.00",
    milestone: "M1",
    status: "Won",
    timestamp: "1:40:23 PM"
  }
];

function TradingDashboard() {
  return (
    <BentoSignals
      signals={signals}
      userEquity={10000}    // $10,000 account
      riskPerTrade={1}      // 1% risk per trade
    />
  );
}
```

## Dependencies

- `lucide-react`: For icons
- `clsx`: For conditional classes
- `tailwind-merge`: For Tailwind class merging
- `React`: ^18+
- `TypeScript`: ^4+

## Integration Steps

1. **Install Dependencies**:
   ```bash
   npm install lucide-react clsx tailwind-merge
   ```

2. **Create Components Folder**:
   ```bash
   mkdir -p src/components/ui
   ```

3. **Copy Components**:
   - `bento-grid.tsx`
   - `bento-signals.tsx`
   - `demo-bento-signals.tsx`

4. **Import and Use**:
   ```tsx
   import { BentoSignals } from './components/ui/bento-signals';
   ```

## Customization

### Styling
- Modify `bg-gray-800/30` for different transparency levels
- Change `backdrop-blur-xl` for different blur intensities
- Adjust color schemes in the component

### Calculations
- Update pip values for different instruments
- Modify risk formulas for different strategies
- Adjust lot size constraints

### Layout
- Change `grid-cols-1 md:grid-cols-3` for different grid layouts
- Modify `colSpan` logic for different card sizing

## Demo

Run the demo to see the component in action:

```bash
npm run dev
# Navigate to /demo route
```

The demo showcases various signal types with calculated lot sizes and P&L projections based on sample data.

## Browser Support

- Modern browsers with CSS Grid support
- Backdrop-filter support (Chrome 76+, Firefox 103+, Safari 9+)
- Fallback styles for older browsers
