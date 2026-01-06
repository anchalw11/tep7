import mongoose from 'mongoose';

const aiChatMessageSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  questionnaireId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Questionnaire'
  },
  sessionId: {
    type: String,
    required: true
  },

  // Message Data
  message: {
    type: String,
    required: true
  },
  response: {
    type: String,
    required: true
  },
  messageType: {
    type: String,
    required: true,
    enum: ['user', 'ai', 'system', 'error']
  },

  // Context Information
  context: {
    type: String
  },

  // Signal Data (if related to signal analysis)
  signalData: {
    symbol: String,
    direction: String,
    entryPrice: Number,
    stopLoss: Number,
    takeProfit: Number,
    confidence: Number,
    analysis: String,
    riskRewardRatio: Number
  },

  // Trade Context (if related to trade analysis)
  tradeContext: {
    tradeId: mongoose.Schema.Types.ObjectId,
    symbol: String,
    pnl: Number,
    outcome: String,
    analysis: String
  },

  // Usage Tracking
  tokensUsed: {
    type: Number,
    default: 0
  },
  modelUsed: {
    type: String,
    default: 'gpt-3.5-turbo'
  },
  responseTime: {
    type: Number // in milliseconds
  },

  // Status and Errors
  isError: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String
  },
  errorCode: {
    type: String
  },

  // User Feedback
  userRating: {
    type: Number,
    min: 1,
    max: 5
  },
  userFeedback: {
    type: String
  },

  // Recommendations and Actions
  recommendations: [{
    type: String
  }],
  suggestedActions: [{
    action: String,
    priority: {
      type: String,
      enum: ['high', 'medium', 'low']
    },
    description: String
  }],

  // Learning Data (for improving AI responses)
  sentiment: {
    type: String,
    enum: ['positive', 'negative', 'neutral', 'confused', 'frustrated', 'satisfied']
  },
  userIntent: {
    type: String,
    enum: ['analysis', 'advice', 'learning', 'complaint', 'praise', 'question', 'clarification']
  },

  // Status
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true,
  collection: 'ai_chat_messages'
});

// Add indexes
aiChatMessageSchema.index({ userId: 1 });
aiChatMessageSchema.index({ questionnaireId: 1 });
aiChatMessageSchema.index({ sessionId: 1 });
aiChatMessageSchema.index({ messageType: 1 });
aiChatMessageSchema.index({ createdAt: 1 });
aiChatMessageSchema.index({ 'signalData.symbol': 1 });
aiChatMessageSchema.index({ isError: 1 });
aiChatMessageSchema.index({ userIntent: 1 });

export default mongoose.model('AIChatMessage', aiChatMessageSchema);
