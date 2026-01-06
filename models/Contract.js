import mongoose from 'mongoose';

const contractSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  questionnaireId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Questionnaire'
  },

  // Contract Status
  signed: {
    type: Boolean,
    default: false
  },
  signedAt: {
    type: Date
  },
  ipAddress: {
    type: String
  },
  userAgent: {
    type: String
  },

  // Contract Details
  contractVersion: {
    type: String,
    default: '1.0'
  },
  acceptedTerms: {
    type: Boolean,
    default: false
  },
  acceptedRiskDisclosure: {
    type: Boolean,
    default: false
  },
  acceptedPrivacyPolicy: {
    type: Boolean,
    default: false
  },

  // Digital Signature
  signatureData: {
    type: String // Base64 encoded signature image
  },
  signatureMethod: {
    type: String,
    enum: ['digital', 'typed', 'checkbox'],
    default: 'checkbox'
  },

  // Contract Content (for audit purposes)
  contractContent: {
    type: String
  },

  // Withdrawal Status
  withdrawalRequested: {
    type: Boolean,
    default: false
  },
  withdrawalReason: {
    type: String
  },
  withdrawalDate: {
    type: Date
  },

  // Status
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true,
  collection: 'contracts'
});

// Add indexes
contractSchema.index({ userId: 1 });
contractSchema.index({ questionnaireId: 1 });
contractSchema.index({ signed: 1 });
contractSchema.index({ signedAt: 1 });
contractSchema.index({ createdAt: 1 });

export default mongoose.model('Contract', contractSchema);
