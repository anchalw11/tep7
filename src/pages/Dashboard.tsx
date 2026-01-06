import { motion } from 'framer-motion';
import { TrendingUp, DollarSign, Activity, AlertCircle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const mockData = [
  { date: 'Jan', profit: 4000 },
  { date: 'Feb', profit: 3000 },
  { date: 'Mar', profit: 5000 },
  { date: 'Apr', profit: 4500 },
  { date: 'May', profit: 6000 },
  { date: 'Jun', profit: 5500 },
];

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-white mb-2">Dashboard</h1>
          <p className="text-slate-400">Welcome back! Here's your trading overview.</p>
        </motion.div>

        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={<DollarSign className="w-8 h-8 text-green-500" />}
            title="Total Profit"
            value="$28,000"
            change="+12.5%"
            positive
          />
          <StatCard
            icon={<Activity className="w-8 h-8 text-blue-500" />}
            title="Win Rate"
            value="68%"
            change="+5.2%"
            positive
          />
          <StatCard
            icon={<TrendingUp className="w-8 h-8 text-purple-500" />}
            title="Active Trades"
            value="12"
            change="+3"
            positive
          />
          <StatCard
            icon={<AlertCircle className="w-8 h-8 text-orange-500" />}
            title="Risk Level"
            value="Medium"
            change="Stable"
          />
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6"
        >
          <h2 className="text-2xl font-semibold text-white mb-6">Performance Chart</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="date" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '8px',
                  color: '#fff',
                }}
              />
              <Line type="monotone" dataKey="profit" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>
    </div>
  );
}

function StatCard({
  icon,
  title,
  value,
  change,
  positive,
}: {
  icon: React.ReactNode;
  title: string;
  value: string;
  change: string;
  positive?: boolean;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:border-blue-500 transition-colors"
    >
      <div className="flex items-start justify-between mb-4">
        {icon}
        <span className={`text-sm ${positive ? 'text-green-500' : 'text-slate-400'}`}>{change}</span>
      </div>
      <p className="text-slate-400 text-sm mb-1">{title}</p>
      <p className="text-3xl font-bold text-white">{value}</p>
    </motion.div>
  );
}
