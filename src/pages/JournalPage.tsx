import { motion } from 'framer-motion';
import { BookOpen, Calendar, TrendingUp, TrendingDown } from 'lucide-react';

const mockTrades = [
  {
    id: 1,
    date: '2024-01-06',
    pair: 'EUR/USD',
    type: 'BUY',
    entry: '1.0850',
    exit: '1.0920',
    profit: '+700',
    status: 'win',
  },
  {
    id: 2,
    date: '2024-01-06',
    pair: 'GBP/USD',
    type: 'SELL',
    entry: '1.2650',
    exit: '1.2620',
    profit: '+300',
    status: 'win',
  },
  {
    id: 3,
    date: '2024-01-05',
    pair: 'USD/JPY',
    type: 'BUY',
    entry: '149.50',
    exit: '149.20',
    profit: '-300',
    status: 'loss',
  },
];

export default function JournalPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 flex items-center gap-4"
        >
          <BookOpen className="w-10 h-10 text-blue-500" />
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Trading Journal</h1>
            <p className="text-slate-400">Track and analyze your trading performance</p>
          </div>
        </motion.div>

        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-900/50">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">Date</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">Pair</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">Type</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">Entry</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">Exit</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">Profit/Loss</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">Status</th>
                </tr>
              </thead>
              <tbody>
                {mockTrades.map((trade, index) => (
                  <motion.tr
                    key={trade.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="border-t border-slate-700 hover:bg-slate-800/30 transition-colors"
                  >
                    <td className="px-6 py-4 text-slate-300 flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      {trade.date}
                    </td>
                    <td className="px-6 py-4 text-white font-medium">{trade.pair}</td>
                    <td className="px-6 py-4">
                      <span
                        className={`px-2 py-1 rounded text-xs font-medium ${
                          trade.type === 'BUY'
                            ? 'bg-green-500/20 text-green-500'
                            : 'bg-red-500/20 text-red-500'
                        }`}
                      >
                        {trade.type}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-slate-300">{trade.entry}</td>
                    <td className="px-6 py-4 text-slate-300">{trade.exit}</td>
                    <td className="px-6 py-4">
                      <span
                        className={`font-semibold flex items-center gap-1 ${
                          trade.status === 'win' ? 'text-green-500' : 'text-red-500'
                        }`}
                      >
                        {trade.status === 'win' ? (
                          <TrendingUp className="w-4 h-4" />
                        ) : (
                          <TrendingDown className="w-4 h-4" />
                        )}
                        {trade.profit}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          trade.status === 'win'
                            ? 'bg-green-500/20 text-green-500'
                            : 'bg-red-500/20 text-red-500'
                        }`}
                      >
                        {trade.status.toUpperCase()}
                      </span>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
