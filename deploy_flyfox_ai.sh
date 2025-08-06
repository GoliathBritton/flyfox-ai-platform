#!/bin/bash
# FLYFOX AI - Complete Deployment Script
# This script deploys the entire FLYFOX AI platform

echo "Starting FLYFOX AI Platform Deployment..."

# 1. Set up environment variables
export FLYFOX_AI_VERSION="1.0.0"
export FLYFOX_AI_DOMAIN="https://flyfoxai.com"
export FLYFOX_AI_CONTACT="john.britton@goliathomniedge.com"

# 2. Install dependencies
echo "Installing dependencies..."
npm install

# 3. Build the React application
echo "Building React application..."
npm run build

# 4. Deploy to Vercel
echo "Deploying to Vercel..."
vercel --prod

# 5. Set up DNS records
echo "Configuring DNS records..."
# DNS configuration will be handled through domain provider

# 6. Initialize databases
echo "Initializing databases..."
python3 -c "
import sqlite3
conn = sqlite3.connect('flyfox_customers.db')
cursor = conn.cursor()

# Create customers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        company TEXT,
        phone TEXT,
        subscription_tier TEXT DEFAULT 'starter',
        subscription_status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        stripe_customer_id TEXT,
        paypal_customer_id TEXT,
        api_calls_used INTEGER DEFAULT 0,
        api_calls_limit INTEGER DEFAULT 5
    )
''')

# Create payments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        amount DECIMAL(10,2) NOT NULL,
        currency TEXT DEFAULT 'USD',
        payment_method TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        stripe_payment_id TEXT,
        paypal_payment_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
''')

conn.commit()
conn.close()
print('Databases initialized successfully')
"

# 7. Test the deployment
echo "Testing deployment..."
curl -f https://app.flyfoxai.com || echo "Deployment test failed"

echo "FLYFOX AI Platform deployment completed!"
echo "Main Application: https://app.flyfoxai.com"
echo "Contact: john.britton@goliathomniedge.com"
echo "Company: Goliath of All Trade Inc."
