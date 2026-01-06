import mongoose from 'mongoose';

const assetPerformanceSchema = new mongoose.Schema({
  symbol: {
    type: String,
    required: true
  },
  trades: {
    type: Number,
    default: 0
  },
  pnl: {
    type: Number,
    default: 0
  },
  winRate: {
    type: Number,
    default: 0
  },
  lastTrade: {
    type: Date
  }
}, { _id: false });

const sessionPerformanceSchema = new mongoose.Schema({
  preferredSession: {
    type: String,
    required: true
  },
  sessionTrades: {
    type: Number,
    default: 0
  },
  sessionPnl: {
    type: Number,
    default: 0
  },
  sessionWinRate: {
    type: Number,
    default: 0
  }
}, { _id: false });

const riskLevelPerformanceSchema = new mongoose.Schema({
  riskPercentage: {
    type: Number,
    required: true
  },
  riskTrades: {
    type: Number,
    default: 0
  },
  riskPnl: {
    type: Number,
    default: 0
  },
  riskWinRate: {
    type: Number,
    default: 0
  }
}, { _id: false });

const dailyStatsSchema = new mongoose.Schema({
  date: {
    type: Date,
    required: true
  },
  pnl: {
    type: Number,
    default: 0
  },
  trades: {
    type: Number,
    default: 0
  },
  winRate: {
    type: Number,
    default: 0
  },
  initialEquity: {
    type: Number,
    default: 0
  },
  endEquity: {
    type: Number,
    default: 0
  }
}, { _id: false });

const userDashboardSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  questionnaireId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Questionnaire'
  },

  // Account Info (from questionnaire)
  propFirm: {
    type: String
  },
  accountType: {
    type: String
  },
  accountSize: {
    type: Number
  },
  currentEquity: {
    type: Number,
    default: 0
  },

  // Core Performance Metrics
  totalPnl: {
    type: Number,
    default: 0
  },
  winRate: {
    type: Number,
    default: 0
  },
  totalTrades: {
    type: Number,
    default: 0
  },
  winningTrades: {
    type: Number,
    default: 0
  },
  losingTrades: {
    type: Number,
    default: 0
  },
  breakevenTrades: {
    type: Number,
    default: 0
  },

  // Detailed P&L Analysis
  grossProfit: {
    type: Number,
    default: 0
  },
  grossLoss: {
    type: Number,
    default: 0
  },
  profitFactor: {
    type: Number,
    default: 0
  },
  averageWin: {
    type: Number,
    default: 0
  },
  averageLoss: {
    type: Number,
    default: 0
  },

  // Risk Metrics
  maxDrawdown: {
    type: Number,
    default: 0
  },
  currentDrawdown: {
    type: Number,
    default: 0
  },
  consecutiveWins: {
    type: Number,
    default: 0
  },
  consecutiveLosses: {
    type: Number,
    default: 0
  },

  // Trading Activity (filtered by questionnaire)
  signalsTaken: {
    type: Number,
    default: 0
  },
  signalsWon: {
    type: Number,
    default: 0
  },
  signalsLost: {
    type: Number,
    default: 0
  },
  signalsBreakeven: {
    type: Number,
    default: 0
  },

  // Asset Performance (filtered by questionnaire assets)
  assetPerformance: [assetPerformanceSchema],

  // Session Performance (filtered by questionnaire session)
  sessionPerformance: sessionPerformanceSchema,

  // Risk Level Performance (filtered by questionnaire risk)
  riskLevelPerformance: riskLevelPerformanceSchema,

  // Daily Statistics
  dailyStats: [dailyStatsSchema],

  // Trading Statistics by Time
  monthlyStats: [{
    month: String, // YYYY-MM format
    pnl: Number,
    trades: Number,
    winRate: Number
  }],

  // Journal Statistics
  journalEntries: {
    type: Number,
    default: 0
  },
  journalWins: {
    type: Number,
    default: 0
  },
  journalLosses: {
    type: Number,
    default: 0
  },
  journalBreakeven: {
    type: Number,
    default: 0
  },

  // AI Coach Statistics
  aiConversations: {
    type: Number,
    default: 0
  },
  aiSignalsAnalyzed: {
    type: Number,
    default: 0
  },
  aiRecommendations: {
    type: Number,
    default: 0
  },

  // Dashboard Preferences (stored for consistency)
  dashboardPreferences: {
    theme: {
      type: String,
      default: 'dark'
    },
    timezone: {
      type: String,
      default: 'Asia/Kolkata'
    },
    currency: {
      type: String,
      default: 'USD'
    },
    compactMode: {
      type: Boolean,
      default: false
    }
  },

  // Data Source and Status
  dataSource: {
    type: String,
    enum: ['real', 'demo', 'backtest'],
    default: 'real'
  },
  isActive: {
    type: Boolean,
    default: true
  },
  lastUpdated: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true,
  collection: 'user_dashboards'
});

// Add indexes
userDashboardSchema.index({ userId: 1 }, { unique: true });
userDashboardSchema.index({ questionnaireId: 1 });
userDashboardSchema.index({ propFirm: 1 });
userDashboardSchema.index({ accountType: 1 });
userDashboardSchema.index({ 'sessionPerformance.preferredSession': 1 });
userDashboardSchema.index({ 'riskLevelPerformance.riskPercentage': 1 });
userDashboardSchema.index({ lastUpdated: 1 });
userDashboardSchema.index({ dataSource: 1 });

export default mongoose.model('UserDashboard', userDashboardSchema);
