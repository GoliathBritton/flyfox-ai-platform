#!/usr/bin/env python3
"""
FLYFOX AI - Customer Management System
Complete user registration, dashboard, and subscription management
"""

import json
import os
import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
import sqlite3
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Customer:
    """FLYFOX AI Customer Data Model"""
    id: str
    email: str
    name: str
    company: str
    subscription_tier: str
    subscription_status: str
    created_at: datetime
    last_login: datetime
    api_key: str
    usage_metrics: Dict

class FlyfoxCustomerManagement:
    """FLYFOX AI Complete Customer Management System"""
    
    def __init__(self, db_path: str = "flyfox_customers.db"):
        self.db_path = db_path
        self.jwt_secret = os.getenv("JWT_SECRET", "flyfox_ai_secret_key")
        self._init_database()
    
    def _init_database(self):
        """Initialize customer database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    company TEXT,
                    password_hash TEXT NOT NULL,
                    subscription_tier TEXT DEFAULT 'none',
                    subscription_status TEXT DEFAULT 'inactive',
                    stripe_customer_id TEXT,
                    paypal_customer_id TEXT,
                    api_key TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_metrics TEXT DEFAULT '{}'
                )
            ''')
            
            # Create usage_logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    service_type TEXT NOT NULL,
                    usage_amount INTEGER DEFAULT 0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            # Create api_keys table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_keys (
                    id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    api_key TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    permissions TEXT DEFAULT 'read',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ FLYFOX AI customer database initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
    
    def register_customer(self, email: str, name: str, password: str, company: str = None) -> Dict:
        """Register a new FLYFOX AI customer"""
        try:
            # Check if customer already exists
            if self._customer_exists(email):
                return {"error": "Customer already exists"}
            
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Generate customer data
            customer_id = str(uuid.uuid4())
            api_key = self._generate_api_key()
            
            # Insert customer into database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO customers (
                    id, email, name, company, password_hash, api_key
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer_id, email, name, company, password_hash, api_key))
            
            conn.commit()
            conn.close()
            
            # Create customer object
            customer = Customer(
                id=customer_id,
                email=email,
                name=name,
                company=company or "",
                subscription_tier="none",
                subscription_status="inactive",
                created_at=datetime.now(),
                last_login=datetime.now(),
                api_key=api_key,
                usage_metrics={}
            )
            
            logger.info(f"✅ Customer registered: {email}")
            return {
                "success": True,
                "customer_id": customer_id,
                "api_key": api_key,
                "message": "FLYFOX AI customer registered successfully"
            }
            
        except Exception as e:
            logger.error(f"❌ Customer registration failed: {e}")
            return {"error": str(e)}
    
    def authenticate_customer(self, email: str, password: str) -> Dict:
        """Authenticate FLYFOX AI customer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, email, name, company, password_hash, subscription_tier, 
                       subscription_status, api_key, created_at, last_login
                FROM customers WHERE email = ?
            ''', (email,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return {"error": "Invalid credentials"}
            
            customer_id, db_email, name, company, password_hash, subscription_tier, \
            subscription_status, api_key, created_at, last_login = result
            
            # Verify password
            if hashlib.sha256(password.encode()).hexdigest() != password_hash:
                return {"error": "Invalid credentials"}
            
            # Update last login
            self._update_last_login(customer_id)
            
            # Generate JWT token
            token = self._generate_jwt_token(customer_id, email)
            
            logger.info(f"✅ Customer authenticated: {email}")
            return {
                "success": True,
                "token": token,
                "customer_id": customer_id,
                "api_key": api_key,
                "subscription_tier": subscription_tier,
                "subscription_status": subscription_status
            }
            
        except Exception as e:
            logger.error(f"❌ Customer authentication failed: {e}")
            return {"error": str(e)}
    
    def get_customer_dashboard(self, customer_id: str) -> Dict:
        """Get FLYFOX AI customer dashboard data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get customer info
            cursor.execute('''
                SELECT email, name, company, subscription_tier, subscription_status, 
                       created_at, last_login, usage_metrics
                FROM customers WHERE id = ?
            ''', (customer_id,))
            
            result = cursor.fetchone()
            if not result:
                return {"error": "Customer not found"}
            
            email, name, company, subscription_tier, subscription_status, \
            created_at, last_login, usage_metrics = result
            
            # Get usage statistics
            cursor.execute('''
                SELECT service_type, SUM(usage_amount) as total_usage
                FROM usage_logs 
                WHERE customer_id = ? 
                GROUP BY service_type
            ''', (customer_id,))
            
            usage_stats = dict(cursor.fetchall())
            
            # Get recent activity
            cursor.execute('''
                SELECT service_type, usage_amount, timestamp
                FROM usage_logs 
                WHERE customer_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''', (customer_id,))
            
            recent_activity = []
            for row in cursor.fetchall():
                recent_activity.append({
                    "service_type": row[0],
                    "usage_amount": row[1],
                    "timestamp": row[2]
                })
            
            conn.close()
            
            # Parse usage metrics
            try:
                usage_metrics = json.loads(usage_metrics) if usage_metrics else {}
            except:
                usage_metrics = {}
            
            dashboard_data = {
                "customer_info": {
                    "id": customer_id,
                    "email": email,
                    "name": name,
                    "company": company,
                    "subscription_tier": subscription_tier,
                    "subscription_status": subscription_status,
                    "created_at": created_at,
                    "last_login": last_login
                },
                "usage_statistics": usage_stats,
                "recent_activity": recent_activity,
                "usage_metrics": usage_metrics,
                "subscription_limits": self._get_subscription_limits(subscription_tier)
            }
            
            logger.info(f"✅ Dashboard data retrieved for customer: {customer_id}")
            return dashboard_data
            
        except Exception as e:
            logger.error(f"❌ Dashboard retrieval failed: {e}")
            return {"error": str(e)}
    
    def update_subscription(self, customer_id: str, tier: str, status: str) -> Dict:
        """Update customer subscription"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE customers 
                SET subscription_tier = ?, subscription_status = ?
                WHERE id = ?
            ''', (tier, status, customer_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Subscription updated for customer {customer_id}: {tier} - {status}")
            return {"success": True, "message": "Subscription updated successfully"}
            
        except Exception as e:
            logger.error(f"❌ Subscription update failed: {e}")
            return {"error": str(e)}
    
    def log_usage(self, customer_id: str, service_type: str, usage_amount: int) -> Dict:
        """Log customer usage"""
        try:
            usage_id = str(uuid.uuid4())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO usage_logs (id, customer_id, service_type, usage_amount)
                VALUES (?, ?, ?, ?)
            ''', (usage_id, customer_id, service_type, usage_amount))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Usage logged: {customer_id} - {service_type} - {usage_amount}")
            return {"success": True, "usage_id": usage_id}
            
        except Exception as e:
            logger.error(f"❌ Usage logging failed: {e}")
            return {"error": str(e)}
    
    def generate_api_key(self, customer_id: str, name: str) -> Dict:
        """Generate new API key for customer"""
        try:
            api_key = self._generate_api_key()
            key_id = str(uuid.uuid4())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO api_keys (id, customer_id, api_key, name)
                VALUES (?, ?, ?, ?)
            ''', (key_id, customer_id, api_key, name))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ API key generated for customer: {customer_id}")
            return {"success": True, "api_key": api_key, "key_id": key_id}
            
        except Exception as e:
            logger.error(f"❌ API key generation failed: {e}")
            return {"error": str(e)}
    
    def validate_api_key(self, api_key: str) -> Dict:
        """Validate API key and return customer info"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT c.id, c.email, c.name, c.subscription_tier, c.subscription_status
                FROM customers c
                JOIN api_keys ak ON c.id = ak.customer_id
                WHERE ak.api_key = ?
            ''', (api_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return {"error": "Invalid API key"}
            
            customer_id, email, name, subscription_tier, subscription_status = result
            
            # Update last used timestamp
            self._update_api_key_usage(api_key)
            
            return {
                "valid": True,
                "customer_id": customer_id,
                "email": email,
                "name": name,
                "subscription_tier": subscription_tier,
                "subscription_status": subscription_status
            }
            
        except Exception as e:
            logger.error(f"❌ API key validation failed: {e}")
            return {"error": str(e)}
    
    def _customer_exists(self, email: str) -> bool:
        """Check if customer exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM customers WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def _generate_api_key(self) -> str:
        """Generate unique API key"""
        return f"flyfox_{uuid.uuid4().hex[:32]}"
    
    def _generate_jwt_token(self, customer_id: str, email: str) -> str:
        """Generate JWT token for customer"""
        payload = {
            "customer_id": customer_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(days=30),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
    
    def _update_last_login(self, customer_id: str):
        """Update customer last login timestamp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        ''', (customer_id,))
        conn.commit()
        conn.close()
    
    def _update_api_key_usage(self, api_key: str):
        """Update API key last used timestamp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE api_keys SET last_used = CURRENT_TIMESTAMP WHERE api_key = ?
        ''', (api_key,))
        conn.commit()
        conn.close()
    
    def _get_subscription_limits(self, tier: str) -> Dict:
        """Get subscription limits for tier"""
        limits = {
            "quantum_starter": {
                "voice_calls": 1000,
                "api_requests": 5000,
                "storage_gb": 10,
                "support_level": "email"
            },
            "quantum_professional": {
                "voice_calls": 5000,
                "api_requests": 25000,
                "storage_gb": 50,
                "support_level": "priority"
            },
            "quantum_enterprise": {
                "voice_calls": -1,  # Unlimited
                "api_requests": -1,  # Unlimited
                "storage_gb": 500,
                "support_level": "dedicated"
            },
            "quantum_elite": {
                "voice_calls": -1,  # Unlimited
                "api_requests": -1,  # Unlimited
                "storage_gb": -1,  # Unlimited
                "support_level": "premium"
            }
        }
        return limits.get(tier, limits["quantum_starter"])

# FLYFOX AI Customer Management Demo
def demo_flyfox_customer_management():
    """Demonstrate FLYFOX AI customer management system"""
    print("🚀 FLYFOX AI - Customer Management System Demo")
    print("=" * 50)
    
    # Initialize customer management
    customer_mgmt = FlyfoxCustomerManagement()
    
    # Demo customer registration
    print("\n1. Registering FLYFOX AI customer...")
    registration = customer_mgmt.register_customer(
        email="demo@flyfoxai.com",
        name="Demo Customer",
        password="secure_password_123",
        company="Demo Corp"
    )
    print(f"✅ Customer registered: {registration}")
    
    # Demo customer authentication
    print("\n2. Authenticating FLYFOX AI customer...")
    auth = customer_mgmt.authenticate_customer(
        email="demo@flyfoxai.com",
        password="secure_password_123"
    )
    print(f"✅ Customer authenticated: {auth}")
    
    # Demo dashboard
    print("\n3. Getting FLYFOX AI customer dashboard...")
    dashboard = customer_mgmt.get_customer_dashboard(auth["customer_id"])
    print(f"✅ Dashboard retrieved: {json.dumps(dashboard, indent=2, default=str)}")
    
    # Demo usage logging
    print("\n4. Logging FLYFOX AI usage...")
    usage = customer_mgmt.log_usage(
        customer_id=auth["customer_id"],
        service_type="quantum_voice_call",
        usage_amount=1
    )
    print(f"✅ Usage logged: {usage}")
    
    # Demo API key generation
    print("\n5. Generating FLYFOX AI API key...")
    api_key = customer_mgmt.generate_api_key(
        customer_id=auth["customer_id"],
        name="Demo API Key"
    )
    print(f"✅ API key generated: {api_key}")
    
    # Demo API key validation
    print("\n6. Validating FLYFOX AI API key...")
    validation = customer_mgmt.validate_api_key(api_key["api_key"])
    print(f"✅ API key validated: {validation}")
    
    print("\n🎉 FLYFOX AI Customer Management System Ready!")
    print("Contact: john.britton@goliathomniedge.com")
    print("Website: https://flyfoxai.com")

if __name__ == "__main__":
    demo_flyfox_customer_management()
