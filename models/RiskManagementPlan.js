import mongoose from 'mongoose';

const tradePlanSchema = new mongoose.Schema({
  trade: {
    type: Number,
    required: true
  },
  balance: {
    type: Number,
    required: true
  },
  riskAmount: {
    type: Number,
    required: true
  },
  profitTarget: {
    type: Number,
    required: true
  }
}, { _id: false });

const riskManagementPlanSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  questionnaireId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Questionnaire',
    required: true
  },

  // Account Details
  accountSize: {
    type: Number,
    required: true
  },
  profitTarget: {
    type: Number,
    required: true
  },
  riskAmount: {
    type: Number,
    required: true
  },

  // Trading Rules
  tradesToPass: {
    type: Number,
    required: true
  },
  maxTradesPerDay: {
    type: Number,
    required: true
  },
  tradingSession: {
    type: String,
    required: true
  },

  // Risk Parameters
  riskPercentage: {
    type: Number,
    required: true
  },
  profitTargetPercentage: {
    type: Number,
    required: true
  },
  maxDailyRisk: {
    type: Number,
    required: true
  },
  dailyRiskAmount: {
    type: Number,
    required: true
  },

  // Assets & Session
  cryptoAssets: [{
    type: String
  }],
  forexAssets: [{
    type: String
  }],
  sessionRecommendation: {
    type: String,
    required: true
  },

  // Trade Plan Matrix
  tradeByTradePlan: [tradePlanSchema],

  // Earnings Projection
  projectedEarnings: {
    type: Number,
    default: 0
  },
  winRate: {
    type: Number,
    default: 0
  },
  compoundingMethod: {
    type: String,
    enum: ['flat', 'compounding'],
    default: 'flat'
  },

  // Position Sizing
  positionSizeInLots: {
    type: Number
  },
  positionSizeInUnits: {
    type: Number
  },
  stopLossPips: {
    type: Number,
    default: 20
  },
  pipValue: {
    type: Number,
    default: 10
  },

  // Status
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true,
  collection: 'risk_management_plans'
});

// Add indexes
riskManagementPlanSchema.index({ userId: 1 });
riskManagementPlanSchema.index({ questionnaireId: 1 });
riskManagementPlanSchema.index({ tradingSession: 1 });
riskManagementPlanSchema.index({ createdAt: 1 });

export default mongoose.model('RiskManagementPlan', riskManagementPlanSchema);
