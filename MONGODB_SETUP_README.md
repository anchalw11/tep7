# MongoDB Setup Guide for TraderEdgePro

## Overview

This guide explains how to set up and use MongoDB as the database for TraderEdgePro instead of PostgreSQL.

## Prerequisites

- Python 3.8+
- MongoDB Atlas account (cloud) or local MongoDB installation
- pip (Python package manager)

## Installation

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. MongoDB Setup

#### Option A: MongoDB Atlas (Recommended)

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a new cluster
3. Create a database user
4. Get your connection string

#### Option B: Local MongoDB

1. Install MongoDB locally
2. Start MongoDB service
3. Use connection string: `mongodb://localhost:27017/traderedgepro`

### 3. Environment Configuration

Create a `.env` file in the root directory:

```bash
# Copy the MongoDB environment file
cp .env.mongodb .env

# Edit the MongoDB URI with your connection string
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/traderedgepro?retryWrites=true&w=majority
```

## Database Collections

The MongoDB setup creates the following collections:

- `users` - User account information
- `questionnaires` - Trading questionnaire responses
- `dashboard_data` - Dashboard performance data
- `payments` - Payment transaction records
- `signals` - Signal tracking data

## API Endpoints

The MongoDB API provides the same endpoints as the PostgreSQL version:

### Health Check
```
GET /api/health
```

### User Management
```
POST /api/enhanced/signup
POST /api/enhanced/questionnaire
GET  /api/enhanced/dashboard/<email>
POST /api/enhanced/dashboard/update
```

### Payments
```
POST /api/enhanced/payment
```

### Signals
```
POST /api/enhanced/signals/track
GET  /api/signals
```

### Admin
```
GET /api/enhanced/admin/users
GET /api/enhanced/admin/stats
```

### Frontend Compatibility
```
GET  /api/dashboard-data
POST /api/dashboard/save
POST /user/progress
GET  /api/trades?userEmail=<email>
```

## Running the Application

### Development

```bash
# Start the backend server
python app.py

# In another terminal, start the frontend
npm run dev
```

### Production

```bash
# Build the frontend
npm run build

# Start the backend (serves both API and static files)
python app.py
```

## Migration from PostgreSQL

If you're migrating from PostgreSQL to MongoDB:

1. Export your data from PostgreSQL
2. Transform the data to match MongoDB document structure
3. Import data using MongoDB tools or scripts
4. Update your environment variables
5. Restart the application

## Data Structure

### User Document Example
```json
{
  "_id": "uuid-string",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password_hash": "hashed_password",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Questionnaire Document Example
```json
{
  "_id": "uuid-string",
  "user_id": "user-uuid",
  "prop_firm": "Goat Funded Trader",
  "account_type": "Two-Step Swing+",
  "account_size": "5000",
  "milestone_access_level": 4,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Troubleshooting

### Connection Issues

1. Check your MongoDB URI is correct
2. Ensure network access is allowed (for Atlas)
3. Verify username/password are correct
4. Check if MongoDB service is running (local)

### Import Errors

1. Install missing Python packages: `pip install pymongo`
2. Check Python path includes the backend directory
3. Verify environment variables are loaded

### Data Issues

1. Check collection names match expectations
2. Verify document structure matches API requirements
3. Use MongoDB Compass to inspect data directly

## Performance Notes

- MongoDB provides better scalability for document-based data
- Indexes should be created on frequently queried fields
- Consider connection pooling for high-traffic applications
- Use MongoDB Atlas for managed cloud hosting

## Support

For issues with MongoDB setup:

1. Check the application logs
2. Verify MongoDB connection
3. Test API endpoints individually
4. Check MongoDB Atlas dashboard for connection issues

## Environment Variables

```bash
# MongoDB
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname

# Flask
FLASK_ENV=development
PORT=5000

# CORS (optional)
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
