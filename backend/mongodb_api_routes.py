#!/usr/bin/env python3
"""
MONGODB API ROUTES FOR TRADEREDGEPRO
Handles ALL data from signup-enhanced, enhanced-payment, questionnaire, and dashboard
Direct connection to MongoDB Atlas
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from pymongo import MongoClient
import hashlib
import uuid
import json
from datetime import datetime, timezone, timedelta
import os
import logging
from typing import Dict, Any, Optional, List
from bson import ObjectId
import urllib.parse
import jwt
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"])

# Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-jwt-secret-key-change-this-in-production')
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://traderedgepro:TraderEdgePro2024!@cluster0.mongodb.net/traderedgepro?retryWrites=true&w=majority')

class DatabaseManager:
    """Manages MongoDB database connections and operations"""

    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client.traderedgepro
            logger.info("✅ MongoDB connection established successfully")
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise

    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        return self.db[collection_name]

    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Insert a single document"""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document"""
        collection = self.get_collection(collection_name)
        result = collection.find_one(query)
        if result:
            result['_id'] = str(result['_id'])
        return result

    def find_many(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> List[Dict[str, Any]]:
        """Find multiple documents"""
        collection = self.get_collection(collection_name)
        query = query or {}
        cursor = collection.find(query)
        if limit:
            cursor = cursor.limit(limit)
        results = list(cursor)
        for result in results:
            result['_id'] = str(result['_id'])
        return results

    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update a single document"""
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, {'$set': update})
        return result.modified_count

    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete a single document"""
        collection = self.get_collection(collection_name)
        result = collection.delete_one(query)
        return result.deleted_count

    def count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents in collection"""
        collection = self.get_collection(collection_name)
        query = query or {}
        return collection.count_documents(query)

# Initialize database manager
db = DatabaseManager()

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_unique_id() -> str:
    """Generate unique user ID"""
    return f"USER_{int(datetime.now().timestamp())}"

def generate_access_token() -> str:
    """Generate access token"""
    return str(uuid.uuid4())

# =============================================
# AUTHENTICATION MIDDLEWARE
# =============================================

def require_auth(f):
    """Authentication middleware for protected endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        # Check if Authorization header exists and is Bearer token
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning("❌ Missing or invalid Authorization header")
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please log in to access this resource',
                'redirect': '/login'
            }), 401

        token = auth_header.split(' ')[1]

        try:
            # Decode JWT token
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            # Token is valid, proceed
            logger.info(f"✅ Authentication successful for user: {payload.get('email', 'unknown')}")
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            logger.warning("❌ Token expired")
            return jsonify({
                'error': 'Token expired',
                'message': 'Your session has expired. Please log in again.',
                'redirect': '/login'
            }), 401
        except jwt.InvalidTokenError:
            logger.warning("❌ Invalid token")
            return jsonify({
                'error': 'Invalid token',
                'message': 'Authentication failed. Please log in again.',
                'redirect': '/login'
            }), 401
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return jsonify({
                'error': 'Authentication error',
                'message': 'An error occurred during authentication.',
                'redirect': '/login'
            }), 401

    return decorated_function

# =============================================
# HEALTH CHECK ENDPOINT
# =============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        collections = db.db.list_collection_names()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'collections': len(collections),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': 'MongoDB API is running'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500

# =============================================
# AUTHENTICATION ENDPOINTS
# =============================================

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """Handle user login with email and password"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Login request: {data}")

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400

        # Find user by email
        user_data = db.find_one('users', {'email': data['email']})

        if not user_data:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Verify password
        if user_data['password_hash'] != hash_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate JWT token
        token_payload = {
            'user_id': str(user_data['_id']),
            'email': user_data['email'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)  # 24 hour expiry
        }

        token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')

        # Return success response
        response_data = {
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user_data['_id']),
                'email': user_data['email'],
                'fullName': f"{user_data['first_name']} {user_data['last_name']}",
                'status': user_data.get('status', 'active')
            }
        }

        logger.info(f"✅ User logged in successfully: {data['email']}")
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/auth/send-otp', methods=['POST', 'OPTIONS'])
def send_otp():
    """Send OTP to email for authentication"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Send OTP request: {data}")

        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400

        # Check if user exists
        user_data = db.find_one('users', {'email': data['email']})

        if not user_data:
            # For security, don't reveal if email exists or not
            return jsonify({
                'success': True,
                'message': 'If an account with this email exists, an OTP has been sent.'
            }), 200

        # Generate a simple OTP (in production, use proper OTP service)
        import random
        otp = str(random.randint(100000, 999999))

        # Store OTP in database with expiry (simplified)
        otp_data = {
            '_id': str(uuid.uuid4()),
            'email': data['email'],
            'otp': otp,
            'created_at': datetime.now(timezone.utc),
            'expires_at': datetime.now(timezone.utc) + timedelta(minutes=10)
        }

        # Remove any existing OTPs for this email
        db.db.otps.delete_many({'email': data['email']})
        db.insert_one('otps', otp_data)

        # In production, send actual email here
        logger.info(f"📧 OTP {otp} generated for {data['email']}")

        return jsonify({
            'success': True,
            'message': 'OTP sent successfully'
        }), 200

    except Exception as e:
        logger.error(f"❌ Send OTP error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/auth/verify-otp', methods=['POST', 'OPTIONS'])
def verify_otp():
    """Verify OTP and login user"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Verify OTP request: {data}")

        if not data.get('email') or not data.get('otpCode'):
            return jsonify({'error': 'Email and OTP code are required'}), 400

        # Find valid OTP
        otp_data = db.find_one('otps', {
            'email': data['email'],
            'otp': data['otpCode'],
            'expires_at': {'$gt': datetime.now(timezone.utc)}
        })

        if not otp_data:
            return jsonify({'error': 'Invalid or expired OTP'}), 401

        # Get user data
        user_data = db.find_one('users', {'email': data['email']})

        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        # Generate JWT token
        token_payload = {
            'user_id': str(user_data['_id']),
            'email': user_data['email'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)  # 24 hour expiry
        }

        token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')

        # Clean up used OTP
        db.db.otps.delete_one({'_id': otp_data['_id']})

        # Return success response
        response_data = {
            'success': True,
            'message': 'OTP verified successfully',
            'token': token,
            'user': {
                'id': str(user_data['_id']),
                'email': user_data['email'],
                'fullName': f"{user_data['first_name']} {user_data['last_name']}",
                'status': user_data.get('status', 'active')
            }
        }

        logger.info(f"✅ OTP verified and user logged in: {data['email']}")
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"❌ Verify OTP error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# =============================================
# SIGNUP-ENHANCED ENDPOINT
# =============================================

@app.route('/api/enhanced/signup', methods=['POST', 'OPTIONS'])
def enhanced_signup():
    """Handle enhanced signup form data"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Enhanced signup request: {data}")

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Check if user already exists
        existing_user = db.find_one('users', {'email': data['email']})

        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409

        # Generate unique identifiers
        user_id = str(uuid.uuid4())
        unique_id = generate_unique_id()
        access_token = generate_access_token()

        # Hash password
        password_hash = hash_password(data['password'])

        # Create user document
        user_document = {
            '_id': user_id,
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'phone': data.get('phone'),
            'company': data.get('company'),
            'country': data.get('country', 'United States'),
            'password_hash': password_hash,
            'selected_plan_name': data.get('selected_plan_name'),
            'selected_plan_price': data.get('selected_plan_price'),
            'selected_plan_period': data.get('selected_plan_period'),
            'selected_plan_description': data.get('selected_plan_description'),
            'agree_to_terms': data.get('agree_to_terms', False),
            'agree_to_marketing': data.get('agree_to_marketing', False),
            'unique_id': unique_id,
            'access_token': access_token,
            'registration_method': 'api',
            'status': 'active',
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc)
        }

        db.insert_one('users', user_document)

        # Return success response
        response_data = {
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user_id,
                'email': data['email'],
                'fullName': f"{data['first_name']} {data['last_name']}",
                'uniqueId': unique_id,
                'status': 'active'
            },
            'access_token': access_token
        }

        logger.info(f"✅ User registered successfully: {data['email']}")
        return jsonify(response_data), 201

    except Exception as e:
        logger.error(f"❌ Enhanced signup error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# =============================================
# ENHANCED-PAYMENT ENDPOINT
# =============================================

@app.route('/api/enhanced/payment', methods=['POST', 'OPTIONS'])
@require_auth
def enhanced_payment():
    """Handle enhanced payment form data"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Enhanced payment request: {data}")

        # Validate required fields
        required_fields = ['user_email', 'plan_name_payment', 'final_price', 'payment_method', 'transaction_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Get user ID from email
        user_data = db.find_one('users', {'email': data['user_email']})

        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        # Generate payment ID
        payment_id = str(uuid.uuid4())

        # Create payment document
        payment_document = {
            '_id': payment_id,
            'user_id': user_data['_id'],
            'user_email': data['user_email'],
            'user_name': f"{user_data['first_name']} {user_data['last_name']}",
            'plan_name_payment': data['plan_name_payment'],
            'original_price': data.get('original_price', data['final_price']),
            'discount_amount': data.get('discount_amount', 0),
            'final_price': data['final_price'],
            'coupon_code': data.get('coupon_code'),
            'coupon_applied': data.get('coupon_applied', False),
            'payment_method': data['payment_method'],
            'payment_provider': data.get('payment_provider'),
            'transaction_id': data['transaction_id'],
            'payment_status': data.get('payment_status', 'completed'),
            'crypto_currency': data.get('crypto_currency'),
            'crypto_network': data.get('crypto_network'),
            'crypto_transaction_hash': data.get('crypto_transaction_hash'),
            'crypto_from_address': data.get('crypto_from_address'),
            'crypto_to_address': data.get('crypto_to_address'),
            'crypto_amount': data.get('crypto_amount'),
            'crypto_verification_status': data.get('crypto_verification_status', 'pending'),
            'stripe_payment_intent_id': data.get('stripe_payment_intent_id'),
            'paypal_order_id': data.get('paypal_order_id'),
            'cryptomus_order_id': data.get('cryptomus_order_id'),
            'payment_completed_at': datetime.now(timezone.utc),
            'created_at': datetime.now(timezone.utc)
        }

        db.insert_one('payments', payment_document)

        # Return success response
        response_data = {
            'success': True,
            'message': 'Payment recorded successfully',
            'payment_id': payment_id,
            'transaction_id': data['transaction_id'],
            'status': 'completed'
        }

        logger.info(f"✅ Payment recorded successfully: {data['user_email']}")
        return jsonify(response_data), 201

    except Exception as e:
        logger.error(f"❌ Enhanced payment error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# =============================================
# QUESTIONNAIRE ENDPOINT
# =============================================

@app.route('/api/enhanced/questionnaire', methods=['POST', 'OPTIONS'])
@require_auth
def enhanced_questionnaire():
    """Handle questionnaire form data"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Enhanced questionnaire request: {data}")

        # Validate required fields
        required_fields = ['user_email', 'prop_firm', 'account_type', 'account_size', 'account_number']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Get user ID from email
        user_data = db.find_one('users', {'email': data['user_email']})

        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        # Generate questionnaire ID
        questionnaire_id = str(uuid.uuid4())
        user_name = f"{user_data['first_name']} {user_data['last_name']}"

        # Determine milestone access level based on account type
        account_type = data['account_type'].lower()
        if 'demo' in account_type or 'beginner' in account_type:
            milestone_access_level = 1
        elif 'standard' in account_type:
            milestone_access_level = 2
        elif 'pro' in account_type or 'experienced' in account_type:
            milestone_access_level = 3
        elif 'funded' in account_type or 'evaluation' in account_type:
            milestone_access_level = 4
        else:
            milestone_access_level = 1  # Default

        # Create questionnaire document
        questionnaire_document = {
            '_id': questionnaire_id,
            'user_id': user_data['_id'],
            'user_email': data['user_email'],
            'user_name': user_name,
            'trades_per_day': data.get('trades_per_day', '1-2'),
            'trading_session': data.get('trading_session', 'any'),
            'crypto_assets': data.get('crypto_assets', []),
            'forex_assets': data.get('forex_assets', []),
            'custom_forex_pairs': data.get('custom_forex_pairs', []),
            'has_account': data.get('has_account', 'no'),
            'account_equity': data.get('account_equity'),
            'prop_firm': data['prop_firm'],
            'account_type': data['account_type'],
            'account_size': data['account_size'],
            'account_number': data['account_number'],
            'risk_percentage': data.get('risk_percentage', 1.0),
            'risk_reward_ratio': data.get('risk_reward_ratio', '2'),
            'challenge_step': data.get('challenge_step'),
            'trading_experience': data.get('trading_experience', 'intermediate'),
            'milestone_access_level': milestone_access_level,
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc)
        }

        db.insert_one('questionnaires', questionnaire_document)

        # Create initial dashboard data entry
        dashboard_id = str(uuid.uuid4())
        initial_balance = data.get('account_equity') if data.get('has_account') == 'yes' else data['account_size']

        dashboard_document = {
            '_id': dashboard_id,
            'user_id': user_data['_id'],
            'questionnaire_id': questionnaire_id,
            'prop_firm': data['prop_firm'],
            'account_type': data['account_type'],
            'account_size': data['account_size'],
            'current_equity': initial_balance,
            'initial_balance': initial_balance,
            'milestone_access_level': milestone_access_level,
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc)
        }

        db.insert_one('dashboard_data', dashboard_document)

        # Return success response
        response_data = {
            'success': True,
            'message': 'Questionnaire completed successfully',
            'questionnaire_id': questionnaire_id,
            'dashboard_id': dashboard_id,
            'milestone_access_level': milestone_access_level
        }

        logger.info(f"✅ Questionnaire completed successfully: {data['user_email']}")
        return jsonify(response_data), 201

    except Exception as e:
        logger.error(f"❌ Enhanced questionnaire error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# =============================================
# DASHBOARD DATA ENDPOINTS
# =============================================

@app.route('/api/enhanced/dashboard/<user_email>', methods=['GET'])
@require_auth
def get_dashboard_data(user_email):
    """Get complete dashboard data for user"""
    try:
        # Get user data
        user_data = db.find_one('users', {'email': user_email})

        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        # Get questionnaire data
        questionnaire = db.find_one('questionnaires', {'user_id': user_data['_id']})

        # Get dashboard data
        dashboard = db.find_one('dashboard_data', {'user_id': user_data['_id']})

        # Get signal tracking data
        signals = db.find_many('signals', {'user_id': user_data['_id']})

        response_data = {
            'success': True,
            'user_profile': {**user_data, **(questionnaire or {})},
            'dashboard_overview': dashboard,
            'signal_performance': signals,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"❌ Get dashboard data error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# =============================================
# ADDITIONAL ENDPOINTS FOR FRONTEND COMPATIBILITY
# =============================================

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data_simple():
    """Simple dashboard data endpoint for frontend compatibility"""
    try:
        # For now, return a basic response - this can be enhanced based on user session
        return jsonify({
            'success': True,
            'data': {
                'totalTrades': 0,
                'winRate': 0,
                'totalPnL': 0,
                'accountBalance': 5000
            }
        }), 200
    except Exception as e:
        logger.error(f"❌ Get dashboard data simple error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/dashboard/save', methods=['POST', 'OPTIONS'])
def save_dashboard_data():
    """Save dashboard data endpoint for frontend compatibility"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Save dashboard data request: {data}")

        # For now, just acknowledge the request - this can be enhanced
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

        # For now, just acknowledge the request - this can be enhanced
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

        # Get user data
        user_data = db.find_one('users', {'email': user_email})
        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        # Get signals (which serve as trades)
        signals = db.find_many('signals', {'user_id': user_data['_id']})

        return jsonify({
            'success': True,
            'trades': signals
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

        # Get signals from database
        signals = db.find_many('signals', {}, limit=limit)

        response = {
            'success': True,
            'signals': signals
        }

        if with_meta:
            response['meta'] = {
                'total': len(signals),
                'limit': limit
            }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"❌ Get signals error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/enhanced/dashboard/update', methods=['POST', 'OPTIONS'])
@require_auth
def update_dashboard_data():
    """Update dashboard data (performance metrics, trades, etc.)"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Dashboard update request: {data}")

        # Validate required fields
        if not data.get('user_email'):
            return jsonify({'error': 'Missing user_email'}), 400

        # Get user ID
        user_data = db.find_one('users', {'email': data['user_email']})

        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        # Update dashboard data
        update_data = {
            'current_equity': data.get('current_equity'),
            'total_pnl': data.get('total_pnl'),
            'total_trades': data.get('total_trades'),
            'winning_trades': data.get('winning_trades'),
            'losing_trades': data.get('losing_trades'),
            'win_rate': data.get('win_rate'),
            'max_drawdown': data.get('max_drawdown'),
            'current_drawdown': data.get('current_drawdown'),
            'daily_pnl': data.get('daily_pnl'),
            'signals_won': data.get('signals_won'),
            'signals_lost': data.get('signals_lost'),
            'last_active': datetime.now(timezone.utc)
        }

        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}

        rows_affected = db.update_one('dashboard_data', {'user_id': user_data['_id']}, update_data)

        response_data = {
            'success': True,
            'message': 'Dashboard data updated successfully',
            'rows_affected': rows_affected
        }

        logger.info(f"✅ Dashboard data updated successfully: {data['user_email']}")
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"❌ Update dashboard data error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# =============================================
# SIGNAL TRACKING ENDPOINTS
# =============================================

@app.route('/api/enhanced/signals/track', methods=['POST', 'OPTIONS'])
@require_auth
def track_signal():
    """Track signal taken by user"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        logger.info(f"Signal tracking request: {data}")

        # Validate required fields
        required_fields = ['user_email', 'signal_id', 'signal_symbol', 'signal_milestone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Get user ID
        user_data = db.find_one('users', {'email': data['user_email']})

        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        # Get dashboard data ID
        dashboard_data = db.find_one('dashboard_data', {'user_id': user_data['_id']})

        # Create signal tracking document
        signal_document = {
            '_id': str(uuid.uuid4()),
            'user_id': user_data['_id'],
            'dashboard_data_id': dashboard_data['_id'] if dashboard_data else None,
            'signal_id': data['signal_id'],
            'signal_symbol': data['signal_symbol'],
            'signal_type': data.get('signal_type'),
            'signal_price': data.get('signal_price'),
            'signal_milestone': data['signal_milestone'],
            'confidence_score': data.get('confidence_score'),
            'taken_by_user': data.get('taken_by_user', True),
            'taken_at': datetime.now(timezone.utc),
            'outcome': data.get('outcome', 'pending'),
            'pnl': data.get('pnl', 0),
            'risk_amount': data.get('risk_amount'),
            'created_at': datetime.now(timezone.utc)
        }

        signal_tracking_id = db.insert_one('signals', signal_document)

        response_data = {
            'success': True,
            'message': 'Signal tracked successfully',
            'signal_tracking_id': signal_tracking_id
        }

        logger.info(f"✅ Signal tracked successfully: {data['user_email']}")
        return jsonify(response_data), 201

    except Exception as e:
        logger.error(f"❌ Signal tracking error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# =============================================
# ADMIN ENDPOINTS
# =============================================

@app.route('/api/enhanced/admin/users', methods=['GET'])
@require_auth
def get_all_users():
    """Get all users with complete profile data"""
    try:
        # Aggregate user data with questionnaires and dashboard info
        users = db.find_many('users', {}, limit=1000)

        # Enrich user data
        enriched_users = []
        for user in users:
            questionnaire = db.find_one('questionnaires', {'user_id': user['_id']})
            dashboard = db.find_one('dashboard_data', {'user_id': user['_id']})

            enriched_user = {
                **user,
                **(questionnaire or {}),
                'dashboard_data': dashboard
            }
            enriched_users.append(enriched_user)

        return jsonify({
            'success': True,
            'users': enriched_users,
            'total_count': len(enriched_users)
        }), 200

    except Exception as e:
        logger.error(f"❌ Get all users error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/enhanced/admin/stats', methods=['GET'])
@require_auth
def get_admin_stats():
    """Get admin statistics"""
    try:
        # Get user stats
        total_users = db.count_documents('users')
        active_users = db.count_documents('users', {'status': 'active'})

        # Get payment stats
        total_payments = db.count_documents('payments')
        completed_payments = db.count_documents('payments', {'payment_status': 'completed'})

        # Calculate revenue
        completed_payments_docs = db.find_many('payments', {'payment_status': 'completed'})
        total_revenue = sum(payment.get('final_price', 0) for payment in completed_payments_docs)

        # Calculate average payment
        avg_payment = total_revenue / completed_payments if completed_payments > 0 else 0

        # Get questionnaire stats
        total_questionnaires = db.count_documents('questionnaires')
        premium_users = db.count_documents('questionnaires', {'milestone_access_level': 4})

        # Get unique prop firms
        questionnaires = db.find_many('questionnaires', {}, limit=1000)
        unique_prop_firms = len(set(q.get('prop_firm') for q in questionnaires if q.get('prop_firm')))

        return jsonify({
            'success': True,
            'user_stats': {
                'total_users': total_users,
                'active_users': active_users,
                'new_users_week': 0,  # Would need date filtering
                'new_users_month': 0  # Would need date filtering
            },
            'payment_stats': {
                'total_payments': total_payments,
                'completed_payments': completed_payments,
                'total_revenue': total_revenue,
                'avg_payment': avg_payment
            },
            'questionnaire_stats': {
                'total_questionnaires': total_questionnaires,
                'unique_prop_firms': unique_prop_firms,
                'premium_users': premium_users
            },
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200

    except Exception as e:
        logger.error(f"❌ Get admin stats error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

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
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    logger.info(f"🚀 Starting MongoDB API on port {port}")
    logger.info(f"🔗 Database: MongoDB Atlas")
    logger.info(f"📊 Available endpoints:")
    logger.info(f"   GET  /api/health - Health check")
    logger.info(f"   POST /api/enhanced/signup - Enhanced signup")
    logger.info(f"   POST /api/enhanced/payment - Enhanced payment")
    logger.info(f"   POST /api/enhanced/questionnaire - Questionnaire")
    logger.info(f"   GET  /api/enhanced/dashboard/<email> - Get dashboard data")
    logger.info(f"   POST /api/enhanced/dashboard/update - Update dashboard")
    logger.info(f"   POST /api/enhanced/signals/track - Track signals")
    logger.info(f"   GET  /api/enhanced/admin/users - Admin user list")
    logger.info(f"   GET  /api/enhanced/admin/stats - Admin statistics")

    app.run(host='0.0.0.0', port=port, debug=debug)
