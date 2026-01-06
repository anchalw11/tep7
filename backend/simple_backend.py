#!/usr/bin/env python3
"""
Simple Backend API for TraderEdgePro - No Database Required
Provides basic API endpoints to resolve 404 errors
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime, timezone
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     supports_credentials=True)

# =============================================
# HEALTH CHECK ENDPOINT
# =============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'fallback',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'message': 'Simple API is running'
    }), 200

# =============================================
# DASHBOARD DATA ENDPOINTS
# =============================================

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data_simple():
    """Simple dashboard data endpoint for frontend compatibility"""
    return jsonify({
        'success': True,
        'data': {
            'totalTrades': 0,
            'winRate': 0,
            'totalPnL': 0,
            'accountBalance': 5000
        }
    }), 200

@app.route('/api/dashboard/save', methods=['POST', 'OPTIONS'])
def save_dashboard_data():
    """Save dashboard data endpoint for frontend compatibility"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Save dashboard data request: {data}")

        # Just acknowledge the request
        return jsonify({
            'success': True,
            'message': 'Dashboard data saved successfully'
        }), 200

    except Exception as e:
        logger.error(f"❌ Save dashboard data error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/user/progress', methods=['POST', 'OPTIONS'])
def save_user_progress():
    """Save user progress endpoint for frontend compatibility"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Save user progress request: {data}")

        # Just acknowledge the request
        return jsonify({
            'success': True,
            'message': 'User progress saved successfully'
        }), 200

    except Exception as e:
        logger.error(f"❌ Save user progress error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/trades', methods=['GET'])
def get_trades():
    """Get trades endpoint for frontend compatibility"""
    try:
        user_email = request.args.get('userEmail')
        if not user_email:
            return jsonify({'error': 'userEmail parameter required'}), 400

        # Get user's recent trades from localStorage simulation
        # In a real implementation, this would come from a database
        # For now, we'll simulate some recent trades for the user

        # Sample recent trades data (this would normally come from database)
        recent_trades = [
            {
                'id': 'trade_001',
                'pair': 'EURUSD',
                'outcome': 'Target Hit',
                'pnl': 50.00,
                'entryTime': '2024-01-04T13:30:48.000Z',  # 1:30:48 PM
                'signalId': 'signal_eurusd_001',
                'userEmail': user_email
            }
        ]

        # Filter trades for this user only (as per requirement)
        user_trades = [trade for trade in recent_trades if trade['userEmail'] == user_email]

        return jsonify({
            'success': True,
            'trades': user_trades
        }), 200

    except Exception as e:
        logger.error(f"❌ Get trades error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/signals', methods=['GET'])
def get_signals():
    """Get signals endpoint for frontend compatibility"""
    try:
        limit = int(request.args.get('limit', 100))
        with_meta = request.args.get('with_meta', 'false').lower() == 'true'

        # Return empty signals array
        response = {
            'success': True,
            'signals': []
        }

        if with_meta:
            response['meta'] = {
                'total': 0,
                'limit': limit
            }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"❌ Get signals error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/journal/entries', methods=['GET'])
def get_journal_entries():
    """Get journal entries endpoint"""
    try:
        user_email = request.args.get('userEmail')
        if not user_email:
            return jsonify({'error': 'userEmail parameter required'}), 400

        # Return empty entries array
        return jsonify({
            'success': True,
            'entries': []
        }), 200

    except Exception as e:
        logger.error(f"❌ Get journal entries error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# =============================================
# AUTH ENDPOINTS (STUB)
# =============================================

@app.route('/api/auth/send-otp', methods=['POST', 'OPTIONS'])
def send_otp():
    """Send OTP endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'OTP sent successfully'
    }), 200

@app.route('/api/auth/verify-otp', methods=['POST', 'OPTIONS'])
def verify_otp():
    """Verify OTP endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'OTP verified successfully',
        'user': {'email': 'test@example.com', 'id': '123'}
    }), 200

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """Login endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user': {'email': 'test@example.com', 'id': '123'}
    }), 200

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    """Register endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Registration successful',
        'user': {'email': 'test@example.com', 'id': '123'}
    }), 200

# =============================================
# PAYMENT ENDPOINTS (STUB)
# =============================================

@app.route('/api/payment/complete', methods=['POST', 'OPTIONS'])
def complete_payment():
    """Complete payment endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Payment completed successfully'
    }), 200

# =============================================
# QUESTIONNAIRE ENDPOINTS (STUB)
# =============================================

@app.route('/api/questionnaire/save', methods=['POST', 'OPTIONS'])
def save_questionnaire():
    """Save questionnaire endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Questionnaire saved successfully'
    }), 200

# =============================================
# RISK MANAGEMENT ENDPOINTS (STUB)
# =============================================

@app.route('/api/risk-management/save', methods=['POST', 'OPTIONS'])
def save_risk_management():
    """Save risk management endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Risk management saved successfully'
    }), 200

# =============================================
# ENHANCED ENDPOINTS (STUB)
# =============================================

@app.route('/api/enhanced/signup', methods=['POST', 'OPTIONS'])
def enhanced_signup():
    """Enhanced signup endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Enhanced signup successful',
        'user': {'email': 'test@example.com', 'id': '123'}
    }), 201

@app.route('/api/enhanced/payment', methods=['POST', 'OPTIONS'])
def enhanced_payment():
    """Enhanced payment endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Enhanced payment successful'
    }), 201

@app.route('/api/enhanced/questionnaire', methods=['POST', 'OPTIONS'])
def enhanced_questionnaire():
    """Enhanced questionnaire endpoint"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Enhanced questionnaire successful'
    }), 201

@app.route('/api/enhanced/dashboard/<user_email>', methods=['GET'])
def get_enhanced_dashboard(user_email):
    """Get enhanced dashboard data"""
    return jsonify({
        'success': True,
        'user_profile': {},
        'dashboard_overview': {},
        'signal_performance': []
    }), 200

@app.route('/api/enhanced/dashboard/update', methods=['POST', 'OPTIONS'])
def update_enhanced_dashboard():
    """Update enhanced dashboard data"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Dashboard updated successfully'
    }), 200

@app.route('/api/enhanced/signals/track', methods=['POST', 'OPTIONS'])
def track_enhanced_signal():
    """Track enhanced signal"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Signal tracked successfully'
    }), 201

@app.route('/api/enhanced/admin/users', methods=['GET'])
def get_admin_users():
    """Get admin users"""
    return jsonify({
        'success': True,
        'users': [],
        'total_count': 0
    }), 200

@app.route('/api/enhanced/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get admin stats"""
    return jsonify({
        'success': True,
        'user_stats': {
            'total_users': 0,
            'active_users': 0,
            'new_users_week': 0,
            'new_users_month': 0
        },
        'payment_stats': {
            'total_payments': 0,
            'completed_payments': 0,
            'total_revenue': 0,
            'avg_payment': 0
        },
        'questionnaire_stats': {
            'total_questionnaires': 0,
            'unique_prop_firms': 0,
            'premium_users': 0
        }
    }), 200

# =============================================
# EMAIL ENDPOINTS (STUB)
# =============================================

@app.route('/api/email/welcome', methods=['POST', 'OPTIONS'])
def send_welcome_email():
    """Send welcome email"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Welcome email sent successfully'
    }), 200

@app.route('/api/email/auth', methods=['POST', 'OPTIONS'])
def send_auth_email():
    """Send auth email"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'Auth email sent successfully'
    }), 200

# =============================================
# COUPON ENDPOINTS (STUB)
# =============================================

@app.route('/api/validate-coupon', methods=['POST', 'OPTIONS'])
def validate_coupon():
    """Validate coupon"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'valid': True,
        'discount': 10,
        'message': 'Coupon validated successfully'
    }), 200

# =============================================
# USERS ENDPOINTS (STUB)
# =============================================

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    return jsonify({
        'success': True,
        'user': {'id': user_id, 'email': 'test@example.com'}
    }), 200

@app.route('/api/users/<user_id>', methods=['PUT', 'OPTIONS'])
def update_user(user_id):
    """Update user"""
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        'success': True,
        'message': 'User updated successfully'
    }), 200

# =============================================
# ERROR HANDLERS
# =============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# =============================================
# MAIN APPLICATION
# =============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3002))
    debug = os.environ.get('FLASK_ENV') == 'development'

    logger.info(f"🚀 Starting Simple API on port {port}")
    logger.info(f"🔗 Database: None (Fallback Mode)")
    logger.info(f"📊 Available endpoints: All API endpoints")

    app.run(host='0.0.0.0', port=port, debug=debug)
