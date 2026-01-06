import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Clock, Target } from 'lucide-react';

const mockSignals = [
  {
    id: 1,
    pair: 'EUR/USD',
    type: 'BUY',
    entry: '1.0850',
    takeProfit: '1.0920',
    stopLoss: '1.0800',
    status: 'active',
    timestamp: '2 min ago',
  },
  {
    id: 2,
    pair: 'GBP/USD',
    type: 'SELL',
    entry: '1.2650',
    takeProfit: '1.2580',
    stopLoss: '1.2700',
    status: 'active',
    timestamp: '15 min ago',
  },
  {
    id: 3,
    pair: 'USD/JPY',
    type: 'BUY',
    entry: '149.50',
    takeProfit: '150.20',
    stopLoss: '149.00',
    status: 'closed',
    timestamp: '1 hour ago',
  },
];

export default function SignalsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-white mb-2">Trading Signals</h1>
          <p className="text-slate-400">AI-powered trading signals updated in real-time</p>
        </motion.div>

        <div className="space-y-4">
          {mockSignals.map((signal, index) => (
            <motion.div
              key={signal.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <SignalCard signal={signal} />
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

function SignalCard({ signal }: { signal: any }) {
  const isBuy = signal.type === 'BUY';

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:border-blue-500 transition-colors">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-4">
          <div className={`p-3 rounded-lg ${isBuy ? 'bg-green-500/20' : 'bg-red-500/20'}`}>
            {isBuy ? (
              <TrendingUp className="w-6 h-6 text-green-500" />
            ) : (
              <TrendingDown className="w-6 h-6 text-red-500" />
            )}
          </div>
          <div>
            <h3 className="text-xl font-semibold text-white">{signal.pair}</h3>
            <p className={`text-sm font-medium ${isBuy ? 'text-green-500' : 'text-red-500'}`}>
              {signal.type}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-slate-400 text-sm">
          <Clock className="w-4 h-4" />
          {signal.timestamp}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <p className="text-slate-400 text-sm mb-1">Entry</p>
          <p className="text-white font-semibold">{signal.entry}</p>
        </div>
        <div>
          <p className="text-slate-400 text-sm mb-1 flex items-center gap-1">
            <Target className="w-3 h-3" /> Take Profit
          </p>
          <p className="text-green-500 font-semibold">{signal.takeProfit}</p>
        </div>
        <div>
          <p className="text-slate-400 text-sm mb-1">Stop Loss</p>
          <p className="text-red-500 font-semibold">{signal.stopLoss}</p>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-slate-700">
        <span
          className={`px-3 py-1 rounded-full text-xs font-medium ${
            signal.status === 'active'
              ? 'bg-blue-500/20 text-blue-500'
              : 'bg-slate-700 text-slate-400'
          }`}
        >
          {signal.status.toUpperCase()}
        </span>
      </div>
    </div>
  );
}
