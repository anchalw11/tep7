import mongoose from 'mongoose';

const journalEntrySchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  questionnaireId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Questionnaire'
  },

  // Trade Details
  date: {
    type: Date,
    required: true
  },
  symbol: {
    type: String,
    required: true
  },
  direction: {
    type: String,
    required: true,
    enum: ['BUY', 'SELL']
  },
  entryPrice: {
    type: Number,
    required: true
  },
  exitPrice: {
    type: Number
  },
  quantity: {
    type: Number,
    required: true
  },

  // Results
  pnl: {
    type: Number
  },
  outcome: {
    type: String,
    enum: ['win', 'loss', 'breakeven']
  },
  notes: {
    type: String
  },
  tags: [{
    type: String
  }],

  // Signal Information (if from signal)
  signalId: {
    type: mongoose.Schema.Types.ObjectId
  },
  signalSource: {
    type: String,
    enum: ['manual', 'ai-generated', 'social', 'news', 'technical'],
    default: 'manual'
  },

  // Market Conditions
  marketCondition: {
    type: String,
    enum: ['trending', 'ranging', 'volatile', 'news-driven', 'economic-event']
  },
  session: {
    type: String,
    enum: ['asian', 'european', 'us', 'overlap']
  },

  // Risk Management
  stopLoss: {
    type: Number
  },
  takeProfit: {
    type: Number
  },
  riskAmount: {
    type: Number
  },
  riskRewardRatio: {
    type: Number
  },

  // Screenshots/Attachments
  screenshotUrl: {
    type: String
  },
  chartScreenshot: {
    type: String
  },

  // Emotional State
  emotionalState: {
    type: String,
    enum: ['confident', 'nervous', 'excited', 'frustrated', 'calm', 'overconfident']
  },
  followedPlan: {
    type: Boolean,
    default: true
  },

  // Lesson Learned
  lessonLearned: {
    type: String
  },
  improvementAreas: [{
    type: String
  }],

  // Status
  isPublic: {
    type: Boolean,
    default: false
  },
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true,
  collection: 'journal_entries'
});

// Add indexes
journalEntrySchema.index({ userId: 1 });
journalEntrySchema.index({ questionnaireId: 1 });
journalEntrySchema.index({ date: 1 });
journalEntrySchema.index({ symbol: 1 });
journalEntrySchema.index({ direction: 1 });
journalEntrySchema.index({ outcome: 1 });
journalEntrySchema.index({ signalSource: 1 });
journalEntrySchema.index({ session: 1 });
journalEntrySchema.index({ createdAt: 1 });

export default mongoose.model('JournalEntry', journalEntrySchema);
