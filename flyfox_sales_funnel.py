#!/usr/bin/env python3
"""
FLYFOX AI - Sales Funnel System
Complete lead capture, trial signup, and sales automation
"""

import json
import os
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
import sqlite3
import uuid
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Lead:
    """FLYFOX AI Lead Data Model"""
    id: str
    email: str
    name: str
    company: str
    phone: str
    source: str
    status: str
    created_at: datetime
    last_contact: datetime
    notes: str

@dataclass
class Trial:
    """FLYFOX AI Trial Data Model"""
    id: str
    lead_id: str
    email: str
    tier: str
    start_date: datetime
    end_date: datetime
    status: str
    usage_metrics: Dict

class FlyfoxSalesFunnel:
    """FLYFOX AI Complete Sales Funnel System"""
    
    def __init__(self, db_path: str = "flyfox_sales.db"):
        self.db_path = db_path
        self._init_database()
        self._setup_email_config()
    
    def _init_database(self):
        """Initialize sales database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create leads table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leads (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    company TEXT,
                    phone TEXT,
                    source TEXT DEFAULT 'website',
                    status TEXT DEFAULT 'new',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_contact TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT DEFAULT ''
                )
            ''')
            
            # Create trials table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trials (
                    id TEXT PRIMARY KEY,
                    lead_id TEXT NOT NULL,
                    email TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_date TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    usage_metrics TEXT DEFAULT '{}',
                    FOREIGN KEY (lead_id) REFERENCES leads (id)
                )
            ''')
            
            # Create sales_activities table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales_activities (
                    id TEXT PRIMARY KEY,
                    lead_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    description TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    outcome TEXT,
                    FOREIGN KEY (lead_id) REFERENCES leads (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ FLYFOX AI sales database initialized")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
    
    def _setup_email_config(self):
        """Setup email configuration"""
        self.email_config = {
            "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "email_user": os.getenv("EMAIL_USER", "john.britton@goliathomniedge.com"),
            "email_password": os.getenv("EMAIL_PASSWORD", ""),
            "from_email": "john.britton@goliathomniedge.com",
            "from_name": "FLYFOX AI"
        }
    
    def capture_lead(self, email: str, name: str, company: str = None, 
                    phone: str = None, source: str = "website") -> Dict:
        """Capture a new FLYFOX AI lead"""
        try:
            # Validate email
            if not self._validate_email(email):
                return {"error": "Invalid email address"}
            
            # Check if lead already exists
            if self._lead_exists(email):
                return {"error": "Lead already exists"}
            
            # Generate lead data
            lead_id = str(uuid.uuid4())
            
            # Insert lead into database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO leads (id, email, name, company, phone, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (lead_id, email, name, company, phone, source))
            
            conn.commit()
            conn.close()
            
            # Send welcome email
            self._send_welcome_email(email, name)
            
            # Log sales activity
            self._log_sales_activity(lead_id, "lead_captured", "New lead captured from website")
            
            logger.info(f"✅ Lead captured: {email}")
            return {
                "success": True,
                "lead_id": lead_id,
                "message": "FLYFOX AI lead captured successfully"
            }
            
        except Exception as e:
            logger.error(f"❌ Lead capture failed: {e}")
            return {"error": str(e)}
    
    def create_trial(self, lead_id: str, tier: str = "quantum_starter") -> Dict:
        """Create FLYFOX AI trial for lead"""
        try:
            # Get lead information
            lead_info = self._get_lead_info(lead_id)
            if not lead_info:
                return {"error": "Lead not found"}
            
            # Check if trial already exists
            if self._trial_exists(lead_id):
                return {"error": "Trial already exists for this lead"}
            
            # Generate trial data
            trial_id = str(uuid.uuid4())
            start_date = datetime.now()
            end_date = start_date + timedelta(days=14)  # 14-day trial
            
            # Insert trial into database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trials (id, lead_id, email, tier, start_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (trial_id, lead_id, lead_info["email"], tier, start_date, end_date))
            
            # Update lead status
            cursor.execute('''
                UPDATE leads SET status = 'trial_active' WHERE id = ?
            ''', (lead_id,))
            
            conn.commit()
            conn.close()
            
            # Send trial activation email
            self._send_trial_activation_email(lead_info["email"], lead_info["name"], tier)
            
            # Log sales activity
            self._log_sales_activity(lead_id, "trial_created", f"Trial created for {tier} tier")
            
            logger.info(f"✅ Trial created: {lead_info['email']} - {tier}")
            return {
                "success": True,
                "trial_id": trial_id,
                "tier": tier,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "message": "FLYFOX AI trial created successfully"
            }
            
        except Exception as e:
            logger.error(f"❌ Trial creation failed: {e}")
            return {"error": str(e)}
    
    def get_lead_info(self, lead_id: str) -> Dict:
        """Get FLYFOX AI lead information"""
        try:
            lead_info = self._get_lead_info(lead_id)
            if not lead_info:
                return {"error": "Lead not found"}
            
            # Get trial information
            trial_info = self._get_trial_info(lead_id)
            
            # Get sales activities
            activities = self._get_sales_activities(lead_id)
            
            lead_data = {
                "lead_info": lead_info,
                "trial_info": trial_info,
                "sales_activities": activities
            }
            
            logger.info(f"✅ Lead info retrieved: {lead_id}")
            return lead_data
            
        except Exception as e:
            logger.error(f"❌ Lead info retrieval failed: {e}")
            return {"error": str(e)}
    
    def update_lead_status(self, lead_id: str, status: str, notes: str = None) -> Dict:
        """Update FLYFOX AI lead status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if notes:
                cursor.execute('''
                    UPDATE leads SET status = ?, notes = ?, last_contact = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, notes, lead_id))
            else:
                cursor.execute('''
                    UPDATE leads SET status = ?, last_contact = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, lead_id))
            
            conn.commit()
            conn.close()
            
            # Log sales activity
            self._log_sales_activity(lead_id, "status_updated", f"Lead status updated to {status}")
            
            logger.info(f"✅ Lead status updated: {lead_id} - {status}")
            return {"success": True, "message": "Lead status updated successfully"}
            
        except Exception as e:
            logger.error(f"❌ Lead status update failed: {e}")
            return {"error": str(e)}
    
    def send_follow_up_email(self, lead_id: str, email_template: str = "follow_up") -> Dict:
        """Send follow-up email to FLYFOX AI lead"""
        try:
            lead_info = self._get_lead_info(lead_id)
            if not lead_info:
                return {"error": "Lead not found"}
            
            # Send email based on template
            if email_template == "follow_up":
                self._send_follow_up_email(lead_info["email"], lead_info["name"])
            elif email_template == "trial_reminder":
                self._send_trial_reminder_email(lead_info["email"], lead_info["name"])
            elif email_template == "conversion":
                self._send_conversion_email(lead_info["email"], lead_info["name"])
            
            # Log sales activity
            self._log_sales_activity(lead_id, "email_sent", f"Follow-up email sent: {email_template}")
            
            logger.info(f"✅ Follow-up email sent: {lead_info['email']} - {email_template}")
            return {"success": True, "message": "Follow-up email sent successfully"}
            
        except Exception as e:
            logger.error(f"❌ Follow-up email failed: {e}")
            return {"error": str(e)}
    
    def get_sales_analytics(self) -> Dict:
        """Get FLYFOX AI sales analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get lead statistics
            cursor.execute('''
                SELECT status, COUNT(*) as count
                FROM leads 
                GROUP BY status
            ''')
            lead_stats = dict(cursor.fetchall())
            
            # Get trial statistics
            cursor.execute('''
                SELECT tier, COUNT(*) as count
                FROM trials 
                GROUP BY tier
            ''')
            trial_stats = dict(cursor.fetchall())
            
            # Get conversion rates
            cursor.execute('''
                SELECT COUNT(*) as total_leads FROM leads
            ''')
            total_leads = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) as total_trials FROM trials
            ''')
            total_trials = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) as converted_leads 
                FROM leads 
                WHERE status = 'converted'
            ''')
            converted_leads = cursor.fetchone()[0]
            
            conn.close()
            
            analytics = {
                "lead_statistics": lead_stats,
                "trial_statistics": trial_stats,
                "conversion_metrics": {
                    "total_leads": total_leads,
                    "total_trials": total_trials,
                    "converted_leads": converted_leads,
                    "lead_to_trial_rate": (total_trials / total_leads * 100) if total_leads > 0 else 0,
                    "trial_to_conversion_rate": (converted_leads / total_trials * 100) if total_trials > 0 else 0
                }
            }
            
            logger.info("✅ Sales analytics retrieved")
            return analytics
            
        except Exception as e:
            logger.error(f"❌ Sales analytics failed: {e}")
            return {"error": str(e)}
    
    def _validate_email(self, email: str) -> bool:
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _lead_exists(self, email: str) -> bool:
        """Check if lead exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM leads WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def _trial_exists(self, lead_id: str) -> bool:
        """Check if trial exists for lead"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM trials WHERE lead_id = ?', (lead_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def _get_lead_info(self, lead_id: str) -> Optional[Dict]:
        """Get lead information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, email, name, company, phone, source, status, 
                   created_at, last_contact, notes
            FROM leads WHERE id = ?
        ''', (lead_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "email": result[1],
                "name": result[2],
                "company": result[3],
                "phone": result[4],
                "source": result[5],
                "status": result[6],
                "created_at": result[7],
                "last_contact": result[8],
                "notes": result[9]
            }
        return None
    
    def _get_trial_info(self, lead_id: str) -> Optional[Dict]:
        """Get trial information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, tier, start_date, end_date, status, usage_metrics
            FROM trials WHERE lead_id = ?
        ''', (lead_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "tier": result[1],
                "start_date": result[2],
                "end_date": result[3],
                "status": result[4],
                "usage_metrics": json.loads(result[5]) if result[5] else {}
            }
        return None
    
    def _get_sales_activities(self, lead_id: str) -> List[Dict]:
        """Get sales activities for lead"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT activity_type, description, timestamp, outcome
            FROM sales_activities 
            WHERE lead_id = ? 
            ORDER BY timestamp DESC
        ''', (lead_id,))
        
        activities = []
        for row in cursor.fetchall():
            activities.append({
                "activity_type": row[0],
                "description": row[1],
                "timestamp": row[2],
                "outcome": row[3]
            })
        
        conn.close()
        return activities
    
    def _log_sales_activity(self, lead_id: str, activity_type: str, description: str):
        """Log sales activity"""
        activity_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sales_activities (id, lead_id, activity_type, description)
            VALUES (?, ?, ?, ?)
        ''', (activity_id, lead_id, activity_type, description))
        conn.commit()
        conn.close()
    
    def _send_welcome_email(self, email: str, name: str):
        """Send welcome email to new lead"""
        subject = "Welcome to FLYFOX AI - Revolutionary Quantum AI Solutions"
        body = f"""
        Dear {name},
        
        Welcome to FLYFOX AI! Thank you for your interest in our revolutionary quantum AI technology.
        
        At FLYFOX AI, we provide:
        • 292x faster training than traditional AI
        • Quantum-enhanced voice calling platform
        • Advanced quantum digital agents
        • Enterprise automation solutions
        
        Our team will be in touch shortly to discuss how FLYFOX AI can transform your business.
        
        Best regards,
        John Britton
        FLYFOX AI
        john.britton@goliathomniedge.com
        https://flyfoxai.com
        """
        
        self._send_email(email, subject, body)
    
    def _send_trial_activation_email(self, email: str, name: str, tier: str):
        """Send trial activation email"""
        subject = "Your FLYFOX AI Trial is Now Active!"
        body = f"""
        Dear {name},
        
        Great news! Your FLYFOX AI {tier} trial is now active.
        
        Trial Details:
        • Tier: {tier}
        • Duration: 14 days
        • Access: Full platform features
        
        Get started today and experience the power of quantum AI technology!
        
        Best regards,
        FLYFOX AI Team
        john.britton@goliathomniedge.com
        https://flyfoxai.com
        """
        
        self._send_email(email, subject, body)
    
    def _send_follow_up_email(self, email: str, name: str):
        """Send follow-up email"""
        subject = "FLYFOX AI - Let's Discuss Your Quantum AI Needs"
        body = f"""
        Dear {name},
        
        I hope this email finds you well. I wanted to follow up on your interest in FLYFOX AI.
        
        Would you be interested in a brief call to discuss how our quantum AI solutions can benefit your business?
        
        We offer:
        • Quantum voice calling platform ($2,999-$49,999/month)
        • Quantum digital agents with NVIDIA ($4,999-$79,999/month)
        • Enterprise automation solutions ($9,999-$149,999/month)
        
        I'm available for a 15-minute consultation at your convenience.
        
        Best regards,
        John Britton
        FLYFOX AI
        john.britton@goliathomniedge.com
        https://flyfoxai.com
        """
        
        self._send_email(email, subject, body)
    
    def _send_trial_reminder_email(self, email: str, name: str):
        """Send trial reminder email"""
        subject = "FLYFOX AI Trial - Don't Miss Out!"
        body = f"""
        Dear {name},
        
        Your FLYFOX AI trial is coming to an end soon. Don't miss out on the opportunity to experience revolutionary quantum AI technology!
        
        Upgrade today to continue enjoying:
        • 292x faster AI processing
        • Quantum-enhanced voice capabilities
        • Advanced digital agents
        • Enterprise automation
        
        Contact us to discuss your upgrade options.
        
        Best regards,
        FLYFOX AI Team
        john.britton@goliathomniedge.com
        https://flyfoxai.com
        """
        
        self._send_email(email, subject, body)
    
    def _send_conversion_email(self, email: str, name: str):
        """Send conversion email"""
        subject = "FLYFOX AI - Welcome to the Quantum Revolution!"
        body = f"""
        Dear {name},
        
        Congratulations on joining FLYFOX AI! You're now part of the quantum AI revolution.
        
        Your account is now active with full access to our quantum AI platform.
        
        If you have any questions or need assistance, our dedicated support team is here to help.
        
        Welcome to the future of AI!
        
        Best regards,
        FLYFOX AI Team
        john.britton@goliathomniedge.com
        https://flyfoxai.com
        """
        
        self._send_email(email, subject, body)
    
    def _send_email(self, to_email: str, subject: str, body: str):
        """Send email using configured SMTP"""
        try:
            if not self.email_config["email_password"]:
                logger.warning("Email password not configured - skipping email send")
                return
            
            msg = f"From: {self.email_config['from_name']} <{self.email_config['from_email']}>\n"
            msg += f"To: {to_email}\n"
            msg += f"Subject: {subject}\n\n"
            msg += body
            
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["email_user"], self.email_config["email_password"])
            server.sendmail(self.email_config["from_email"], to_email, msg)
            server.quit()
            
            logger.info(f"✅ Email sent to: {to_email}")
            
        except Exception as e:
            logger.error(f"❌ Email send failed: {e}")

# FLYFOX AI Sales Funnel Demo
def demo_flyfox_sales_funnel():
    """Demonstrate FLYFOX AI sales funnel system"""
    print("🚀 FLYFOX AI - Sales Funnel System Demo")
    print("=" * 50)
    
    # Initialize sales funnel
    sales_funnel = FlyfoxSalesFunnel()
    
    # Demo lead capture
    print("\n1. Capturing FLYFOX AI lead...")
    lead = sales_funnel.capture_lead(
        email="demo@flyfoxai.com",
        name="Demo Lead",
        company="Demo Corp",
        phone="+1-555-0123",
        source="website"
    )
    print(f"✅ Lead captured: {lead}")
    
    # Demo trial creation
    print("\n2. Creating FLYFOX AI trial...")
    trial = sales_funnel.create_trial(
        lead_id=lead["lead_id"],
        tier="quantum_starter"
    )
    print(f"✅ Trial created: {trial}")
    
    # Demo lead info retrieval
    print("\n3. Getting FLYFOX AI lead info...")
    lead_info = sales_funnel.get_lead_info(lead["lead_id"])
    print(f"✅ Lead info retrieved: {json.dumps(lead_info, indent=2, default=str)}")
    
    # Demo follow-up email
    print("\n4. Sending FLYFOX AI follow-up email...")
    email = sales_funnel.send_follow_up_email(
        lead_id=lead["lead_id"],
        email_template="follow_up"
    )
    print(f"✅ Follow-up email sent: {email}")
    
    # Demo sales analytics
    print("\n5. Getting FLYFOX AI sales analytics...")
    analytics = sales_funnel.get_sales_analytics()
    print(f"✅ Sales analytics: {json.dumps(analytics, indent=2, default=str)}")
    
    print("\n🎉 FLYFOX AI Sales Funnel System Ready!")
    print("Contact: john.britton@goliathomniedge.com")
    print("Website: https://flyfoxai.com")

if __name__ == "__main__":
    demo_flyfox_sales_funnel()
