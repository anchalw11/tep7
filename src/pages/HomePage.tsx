import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { TrendingUp, Shield, BarChart3, Brain, ArrowRight } from 'lucide-react';
import type { ReactNode } from 'react';

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <nav className="container mx-auto px-6 py-6 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <TrendingUp className="w-8 h-8 text-blue-500" />
          <span className="text-2xl font-bold text-white">Trader Edge Pro</span>
        </div>
        <div className="flex gap-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            Dashboard
          </button>
        </div>
      </nav>

      <main className="container mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-4xl mx-auto"
        >
          <h1 className="text-6xl font-bold text-white mb-6">
            AI-Powered Trading Platform
          </h1>
          <p className="text-xl text-slate-300 mb-12">
            Advanced trading signals, risk management, and comprehensive analytics for professional traders
          </p>
          <button
            onClick={() => navigate('/signals')}
            className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white text-lg rounded-lg transition-colors inline-flex items-center gap-2"
          >
            Get Started
            <ArrowRight className="w-5 h-5" />
          </button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="grid md:grid-cols-4 gap-8 mt-24"
        >
          <FeatureCard
            icon={<Brain className="w-12 h-12 text-blue-500" />}
            title="AI Signals"
            description="Real-time trading signals powered by advanced machine learning algorithms"
          />
          <FeatureCard
            icon={<Shield className="w-12 h-12 text-green-500" />}
            title="Risk Management"
            description="Comprehensive risk management tools to protect your capital"
          />
          <FeatureCard
            icon={<BarChart3 className="w-12 h-12 text-purple-500" />}
            title="Analytics"
            description="Detailed performance analytics and trading insights"
          />
          <FeatureCard
            icon={<TrendingUp className="w-12 h-12 text-orange-500" />}
            title="Trading Journal"
            description="Track and analyze all your trades in one place"
          />
        </motion.div>
      </main>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: ReactNode; title: string; description: string }) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:border-blue-500 transition-colors">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-slate-400">{description}</p>
    </div>
  );
}
