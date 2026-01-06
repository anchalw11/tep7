import mongoose from 'mongoose';

const questionnaireSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },

  // Account Information
  propFirm: {
    type: String,
    required: true
  },
  accountType: {
    type: String,
    required: true
  },
  accountSize: {
    type: Number,
    required: true
  },
  hasAccount: {
    type: Boolean,
    required: true
  },
  accountEquity: {
    type: Number
  },
  accountNumber: {
    type: String,
    required: true
  },

  // Trading Preferences
  tradesPerDay: {
    type: String,
    required: true,
    enum: ['1-2', '3-5', '6-10', '10+']
  },
  tradingSession: {
    type: String,
    required: true,
    enum: ['asian', 'european', 'us', 'any']
  },
  riskPercentage: {
    type: Number,
    required: true,
    min: 0.1,
    max: 10
  },
  riskRewardRatio: {
    type: Number,
    required: true,
    min: 1,
    max: 4
  },

  // Trading Assets
  cryptoAssets: [{
    type: String
  }],
  forexAssets: [{
    type: String
  }],
  customForexPairs: [{
    type: String
  }],

  // Personal Information
  firstName: {
    type: String
  },
  lastName: {
    type: String
  },
  phone: {
    type: String
  },
  country: {
    type: String,
    required: true
  },

  // Status
  completed: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: true,
  collection: 'questionnaires'
});

// Add indexes
questionnaireSchema.index({ userId: 1 });
questionnaireSchema.index({ completed: 1 });
questionnaireSchema.index({ propFirm: 1 });
questionnaireSchema.index({ accountType: 1 });
questionnaireSchema.index({ createdAt: 1 });

export default mongoose.model('Questionnaire', questionnaireSchema);
