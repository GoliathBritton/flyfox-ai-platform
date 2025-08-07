"""
Unit tests for FLYFOX AI Sales Funnel System
Tests lead capture, conversion tracking, and trial management
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
import sqlite3
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from flyfox_sales_funnel import FlyfoxSalesFunnel


class TestFlyfoxSalesFunnel(unittest.TestCase):
    """Test cases for FlyfoxSalesFunnel"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.sales_system = FlyfoxSalesFunnel(db_path=self.temp_db.name)
        self.test_lead_data = {
            "email": "test@flyfoxai.com",
            "name": "Test Lead",
            "company": "Test Corp",
            "phone": "+1234567890",
            "source": "website",
            "campaign": "summer_2024"
        }
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove temporary database
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_sales_system_initialization(self):
        """Test that sales system initializes correctly"""
        self.assertIsNotNone(self.sales_system)
        self.assertIsNotNone(self.sales_system.db_path)
        
        # Check that database tables are created
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            self.assertIn("leads", tables)
            self.assertIn("conversions", tables)
            self.assertIn("trials", tables)
            self.assertIn("campaigns", tables)
    
    def test_capture_lead_success(self):
        """Test successful lead capture"""
        result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        self.assertTrue(result["success"])
        self.assertIn("lead_id", result)
        self.assertEqual(result["email"], self.test_lead_data["email"])
        self.assertEqual(result["name"], self.test_lead_data["name"])
        self.assertEqual(result["status"], "new")
    
    def test_capture_lead_with_optional_fields(self):
        """Test lead capture with all optional fields"""
        result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"],
            phone=self.test_lead_data["phone"],
            source=self.test_lead_data["source"],
            campaign=self.test_lead_data["campaign"]
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["phone"], self.test_lead_data["phone"])
        self.assertEqual(result["source"], self.test_lead_data["source"])
        self.assertEqual(result["campaign"], self.test_lead_data["campaign"])
    
    def test_capture_lead_duplicate_email(self):
        """Test lead capture with duplicate email"""
        # Capture first lead
        result1 = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        self.assertTrue(result1["success"])
        
        # Try to capture lead with same email
        result2 = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name="Another Lead",
            company="Another Corp"
        )
        
        # Should update existing lead instead of creating duplicate
        self.assertTrue(result2["success"])
        self.assertEqual(result2["lead_id"], result1["lead_id"])
    
    def test_capture_lead_invalid_email(self):
        """Test lead capture with invalid email"""
        result = self.sales_system.capture_lead(
            email="invalid-email",
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_update_lead_status(self):
        """Test updating lead status"""
        # First capture a lead
        capture_result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        lead_id = capture_result["lead_id"]
        
        # Update lead status
        result = self.sales_system.update_lead_status(lead_id, "contacted")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["status"], "contacted")
    
    def test_get_lead_details(self):
        """Test retrieving lead details"""
        # First capture a lead
        capture_result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        lead_id = capture_result["lead_id"]
        
        # Get lead details
        result = self.sales_system.get_lead_details(lead_id)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["email"], self.test_lead_data["email"])
        self.assertEqual(result["name"], self.test_lead_data["name"])
        self.assertEqual(result["company"], self.test_lead_data["company"])
    
    def test_create_trial_success(self):
        """Test successful trial creation"""
        # First capture a lead
        capture_result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        lead_id = capture_result["lead_id"]
        
        # Create trial
        result = self.sales_system.create_trial(lead_id, "quantum_starter")
        
        self.assertTrue(result["success"])
        self.assertIn("trial_id", result)
        self.assertEqual(result["plan"], "quantum_starter")
        self.assertEqual(result["status"], "active")
        
        # Check trial duration
        self.assertIn("start_date", result)
        self.assertIn("end_date", result)
    
    def test_create_trial_invalid_lead(self):
        """Test trial creation with invalid lead ID"""
        result = self.sales_system.create_trial("invalid_lead_id", "quantum_starter")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_create_trial_invalid_plan(self):
        """Test trial creation with invalid plan"""
        # First capture a lead
        capture_result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        lead_id = capture_result["lead_id"]
        
        # Try to create trial with invalid plan
        result = self.sales_system.create_trial(lead_id, "invalid_plan")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_track_conversion(self):
        """Test conversion tracking"""
        # First capture a lead and create trial
        capture_result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        lead_id = capture_result["lead_id"]
        trial_result = self.sales_system.create_trial(lead_id, "quantum_starter")
        trial_id = trial_result["trial_id"]
        
        # Track conversion
        result = self.sales_system.track_conversion(
            lead_id=lead_id,
            trial_id=trial_id,
            conversion_type="trial_to_paid",
            amount=299900
        )
        
        self.assertTrue(result["success"])
        self.assertIn("conversion_id", result)
        self.assertEqual(result["conversion_type"], "trial_to_paid")
        self.assertEqual(result["amount"], 299900)
    
    def test_get_conversion_analytics(self):
        """Test conversion analytics"""
        # Create multiple leads and conversions for analytics
        for i in range(5):
            capture_result = self.sales_system.capture_lead(
                email=f"test{i}@flyfoxai.com",
                name=f"Test Lead {i}",
                company=f"Test Corp {i}"
            )
            
            trial_result = self.sales_system.create_trial(
                capture_result["lead_id"], 
                "quantum_starter"
            )
            
            self.sales_system.track_conversion(
                lead_id=capture_result["lead_id"],
                trial_id=trial_result["trial_id"],
                conversion_type="trial_to_paid",
                amount=299900
            )
        
        # Get analytics
        result = self.sales_system.get_conversion_analytics()
        
        self.assertTrue(result["success"])
        self.assertIn("total_leads", result)
        self.assertIn("total_conversions", result)
        self.assertIn("conversion_rate", result)
        self.assertIn("total_revenue", result)
        
        self.assertEqual(result["total_leads"], 5)
        self.assertEqual(result["total_conversions"], 5)
        self.assertEqual(result["conversion_rate"], 100.0)
        self.assertEqual(result["total_revenue"], 1499500)  # 5 * 299900
    
    def test_get_campaign_performance(self):
        """Test campaign performance tracking"""
        # Create leads with different campaigns
        campaigns = ["summer_2024", "winter_2024", "spring_2024"]
        
        for campaign in campaigns:
            for i in range(3):
                self.sales_system.capture_lead(
                    email=f"test_{campaign}_{i}@flyfoxai.com",
                    name=f"Test Lead {i}",
                    company=f"Test Corp {i}",
                    campaign=campaign
                )
        
        # Get campaign performance
        result = self.sales_system.get_campaign_performance()
        
        self.assertTrue(result["success"])
        self.assertIn("campaigns", result)
        
        for campaign_data in result["campaigns"]:
            self.assertIn("campaign_name", campaign_data)
            self.assertIn("lead_count", campaign_data)
            self.assertEqual(campaign_data["lead_count"], 3)
    
    def test_send_follow_up_email(self):
        """Test follow-up email sending"""
        # First capture a lead
        capture_result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        lead_id = capture_result["lead_id"]
        
        # Send follow-up email
        result = self.sales_system.send_follow_up_email(
            lead_id=lead_id,
            email_template="welcome_series_1"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("email_id", result)
        self.assertEqual(result["template"], "welcome_series_1")
    
    def test_schedule_demo(self):
        """Test demo scheduling"""
        # First capture a lead
        capture_result = self.sales_system.capture_lead(
            email=self.test_lead_data["email"],
            name=self.test_lead_data["name"],
            company=self.test_lead_data["company"]
        )
        
        lead_id = capture_result["lead_id"]
        
        # Schedule demo
        demo_date = datetime.now() + timedelta(days=2)
        result = self.sales_system.schedule_demo(
            lead_id=lead_id,
            demo_date=demo_date,
            demo_type="product_demo"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("demo_id", result)
        self.assertEqual(result["demo_type"], "product_demo")
        self.assertEqual(result["status"], "scheduled")


class TestLeadScoring(unittest.TestCase):
    """Test cases for lead scoring"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.sales_system = FlyfoxSalesFunnel(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_calculate_lead_score(self):
        """Test lead score calculation"""
        # Create a lead with various attributes
        capture_result = self.sales_system.capture_lead(
            email="test@flyfoxai.com",
            name="Test Lead",
            company="Enterprise Corp",
            phone="+1234567890",
            source="website",
            campaign="enterprise_2024"
        )
        
        lead_id = capture_result["lead_id"]
        
        # Calculate lead score
        result = self.sales_system.calculate_lead_score(lead_id)
        
        self.assertTrue(result["success"])
        self.assertIn("score", result)
        self.assertIsInstance(result["score"], int)
        self.assertTrue(0 <= result["score"] <= 100)
    
    def test_lead_scoring_factors(self):
        """Test different lead scoring factors"""
        # Test enterprise company (higher score)
        enterprise_result = self.sales_system.capture_lead(
            email="enterprise@flyfoxai.com",
            name="Enterprise Lead",
            company="Fortune 500 Corp",
            source="website"
        )
        
        enterprise_score = self.sales_system.calculate_lead_score(enterprise_result["lead_id"])
        
        # Test small business (lower score)
        small_business_result = self.sales_system.capture_lead(
            email="small@flyfoxai.com",
            name="Small Business Lead",
            company="Small Corp",
            source="website"
        )
        
        small_business_score = self.sales_system.calculate_lead_score(small_business_result["lead_id"])
        
        # Enterprise should have higher score
        self.assertGreater(enterprise_score["score"], small_business_score["score"])
    
    def test_lead_qualification(self):
        """Test lead qualification based on score"""
        # Create a high-scoring lead
        capture_result = self.sales_system.capture_lead(
            email="qualified@flyfoxai.com",
            name="Qualified Lead",
            company="Large Enterprise",
            phone="+1234567890",
            source="referral"
        )
        
        lead_id = capture_result["lead_id"]
        
        # Check qualification
        result = self.sales_system.qualify_lead(lead_id)
        
        self.assertTrue(result["success"])
        self.assertIn("qualified", result)
        self.assertIn("score", result)
        self.assertIn("recommendations", result)


class TestAutomationWorkflows(unittest.TestCase):
    """Test cases for automation workflows"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.sales_system = FlyfoxSalesFunnel(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_welcome_series_automation(self):
        """Test welcome series automation"""
        # Capture a lead
        capture_result = self.sales_system.capture_lead(
            email="automation@flyfoxai.com",
            name="Automation Test",
            company="Test Corp"
        )
        
        lead_id = capture_result["lead_id"]
        
        # Trigger welcome series
        result = self.sales_system.trigger_welcome_series(lead_id)
        
        self.assertTrue(result["success"])
        self.assertIn("emails_scheduled", result)
        self.assertGreater(result["emails_scheduled"], 0)
    
    def test_demo_reminder_automation(self):
        """Test demo reminder automation"""
        # Schedule a demo
        capture_result = self.sales_system.capture_lead(
            email="demo@flyfoxai.com",
            name="Demo Test",
            company="Demo Corp"
        )
        
        lead_id = capture_result["lead_id"]
        demo_date = datetime.now() + timedelta(days=1)
        
        demo_result = self.sales_system.schedule_demo(
            lead_id=lead_id,
            demo_date=demo_date,
            demo_type="product_demo"
        )
        
        # Set up reminders
        result = self.sales_system.setup_demo_reminders(demo_result["demo_id"])
        
        self.assertTrue(result["success"])
        self.assertIn("reminders_scheduled", result)
    
    def test_trial_expiration_automation(self):
        """Test trial expiration automation"""
        # Create a trial
        capture_result = self.sales_system.capture_lead(
            email="trial@flyfoxai.com",
            name="Trial Test",
            company="Trial Corp"
        )
        
        lead_id = capture_result["lead_id"]
        trial_result = self.sales_system.create_trial(lead_id, "quantum_starter")
        
        # Set up expiration reminders
        result = self.sales_system.setup_trial_expiration_reminders(trial_result["trial_id"])
        
        self.assertTrue(result["success"])
        self.assertIn("reminders_scheduled", result)


class TestDataValidation(unittest.TestCase):
    """Test cases for data validation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.sales_system = FlyfoxSalesFunnel(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_validate_lead_data(self):
        """Test lead data validation"""
        # Valid lead data
        valid_data = {
            "email": "test@flyfoxai.com",
            "name": "Test Lead",
            "company": "Test Corp"
        }
        
        result = self.sales_system.validate_lead_data(valid_data)
        self.assertTrue(result["valid"])
        
        # Invalid lead data (missing required fields)
        invalid_data = {
            "email": "test@flyfoxai.com"
            # Missing name and company
        }
        
        result = self.sales_system.validate_lead_data(invalid_data)
        self.assertFalse(result["valid"])
        self.assertIn("errors", result)
    
    def test_validate_campaign_data(self):
        """Test campaign data validation"""
        # Valid campaign data
        valid_campaign = {
            "name": "summer_2024",
            "start_date": "2024-06-01",
            "end_date": "2024-08-31"
        }
        
        result = self.sales_system.validate_campaign_data(valid_campaign)
        self.assertTrue(result["valid"])
        
        # Invalid campaign data
        invalid_campaign = {
            "name": "",  # Empty name
            "start_date": "2024-06-01",
            "end_date": "2024-05-31"  # End before start
        }
        
        result = self.sales_system.validate_campaign_data(invalid_campaign)
        self.assertFalse(result["valid"])
        self.assertIn("errors", result)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
