"""
Integration tests for FLYFOX AI Complete Workflow
Tests the full customer journey from lead capture to payment processing
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
from flyfox_customer_management import FlyfoxCustomerManagement
from flyfox_payment_integration import FlyfoxPaymentSystem


class TestCompleteCustomerWorkflow(unittest.TestCase):
    """Test the complete customer journey workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary databases for testing
        self.temp_sales_db = tempfile.NamedTemporaryFile(delete=False, suffix='_sales.db')
        self.temp_sales_db.close()
        
        self.temp_customer_db = tempfile.NamedTemporaryFile(delete=False, suffix='_customer.db')
        self.temp_customer_db.close()
        
        # Initialize all systems
        self.sales_system = FlyfoxSalesFunnel(db_path=self.temp_sales_db.name)
        self.customer_system = FlyfoxCustomerManagement(db_path=self.temp_customer_db.name)
        self.payment_system = FlyfoxPaymentSystem()
        
        self.test_customer_data = {
            "email": "workflow@flyfoxai.com",
            "name": "Workflow Test User",
            "company": "Workflow Test Corp",
            "phone": "+1234567890",
            "password": "secure_password_123"
        }
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove temporary databases
        for db_path in [self.temp_sales_db.name, self.temp_customer_db.name]:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_complete_customer_journey(self):
        """Test the complete customer journey from lead to paid customer"""
        
        # Step 1: Lead Capture
        print("🔄 Step 1: Capturing lead...")
        lead_result = self.sales_system.capture_lead(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            company=self.test_customer_data["company"],
            phone=self.test_customer_data["phone"]
        )
        
        self.assertTrue(lead_result["success"])
        lead_id = lead_result["lead_id"]
        print(f"✅ Lead captured with ID: {lead_id}")
        
        # Step 2: Lead Qualification
        print("🔄 Step 2: Qualifying lead...")
        qualification_result = self.sales_system.qualify_lead(lead_id)
        
        self.assertTrue(qualification_result["success"])
        self.assertIn("qualified", qualification_result)
        print(f"✅ Lead qualified: {qualification_result['qualified']}")
        
        # Step 3: Customer Registration
        print("🔄 Step 3: Registering customer...")
        registration_result = self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        self.assertTrue(registration_result["success"])
        customer_id = registration_result["customer_id"]
        print(f"✅ Customer registered with ID: {customer_id}")
        
        # Step 4: Trial Creation
        print("🔄 Step 4: Creating trial...")
        trial_result = self.sales_system.create_trial(lead_id, "quantum_starter")
        
        self.assertTrue(trial_result["success"])
        trial_id = trial_result["trial_id"]
        print(f"✅ Trial created with ID: {trial_id}")
        
        # Step 5: Customer Authentication
        print("🔄 Step 5: Authenticating customer...")
        auth_result = self.customer_system.authenticate_customer(
            email=self.test_customer_data["email"],
            password=self.test_customer_data["password"]
        )
        
        self.assertTrue(auth_result["success"])
        session_token = auth_result["session_token"]
        print(f"✅ Customer authenticated with session token")
        
        # Step 6: Payment Processing
        print("🔄 Step 6: Processing payment...")
        with patch('stripe.PaymentIntent.create') as mock_payment:
            mock_payment.return_value = Mock(
                id="pi_test_workflow",
                amount=299900,
                currency="usd",
                status="succeeded"
            )
            
            payment_result = self.payment_system.process_payment(
                amount=299900,
                currency="usd",
                customer_id=customer_id
            )
            
            self.assertTrue(payment_result["success"])
            payment_id = payment_result["payment_id"]
            print(f"✅ Payment processed with ID: {payment_id}")
        
        # Step 7: Conversion Tracking
        print("🔄 Step 7: Tracking conversion...")
        conversion_result = self.sales_system.track_conversion(
            lead_id=lead_id,
            trial_id=trial_id,
            conversion_type="trial_to_paid",
            amount=299900
        )
        
        self.assertTrue(conversion_result["success"])
        conversion_id = conversion_result["conversion_id"]
        print(f"✅ Conversion tracked with ID: {conversion_id}")
        
        # Step 8: Verify Final State
        print("🔄 Step 8: Verifying final state...")
        
        # Verify lead status
        lead_details = self.sales_system.get_lead_details(lead_id)
        self.assertEqual(lead_details["status"], "converted")
        
        # Verify customer profile
        customer_profile = self.customer_system.get_customer_profile(customer_id)
        self.assertEqual(customer_profile["email"], self.test_customer_data["email"])
        
        # Verify trial status
        trial_details = self.sales_system.get_trial_details(trial_id)
        self.assertEqual(trial_details["status"], "converted")
        
        print("✅ Complete workflow test passed!")
    
    def test_lead_to_trial_workflow(self):
        """Test lead capture to trial creation workflow"""
        
        # Capture lead
        lead_result = self.sales_system.capture_lead(
            email="trial@flyfoxai.com",
            name="Trial Test User",
            company="Trial Corp"
        )
        
        self.assertTrue(lead_result["success"])
        lead_id = lead_result["lead_id"]
        
        # Update lead status to qualified
        self.sales_system.update_lead_status(lead_id, "qualified")
        
        # Create trial
        trial_result = self.sales_system.create_trial(lead_id, "quantum_starter")
        
        self.assertTrue(trial_result["success"])
        self.assertEqual(trial_result["plan"], "quantum_starter")
        self.assertEqual(trial_result["status"], "active")
        
        # Verify lead status updated
        lead_details = self.sales_system.get_lead_details(lead_id)
        self.assertEqual(lead_details["status"], "trial")
    
    def test_trial_to_paid_conversion(self):
        """Test trial to paid conversion workflow"""
        
        # Setup: Create lead and trial
        lead_result = self.sales_system.capture_lead(
            email="conversion@flyfoxai.com",
            name="Conversion Test",
            company="Conversion Corp"
        )
        
        lead_id = lead_result["lead_id"]
        trial_result = self.sales_system.create_trial(lead_id, "quantum_starter")
        trial_id = trial_result["trial_id"]
        
        # Register customer
        customer_result = self.customer_system.register_customer(
            email="conversion@flyfoxai.com",
            name="Conversion Test",
            password="password123"
        )
        
        customer_id = customer_result["customer_id"]
        
        # Process payment
        with patch('stripe.PaymentIntent.create') as mock_payment:
            mock_payment.return_value = Mock(
                id="pi_test_conversion",
                amount=299900,
                currency="usd",
                status="succeeded"
            )
            
            payment_result = self.payment_system.process_payment(
                amount=299900,
                currency="usd",
                customer_id=customer_id
            )
            
            self.assertTrue(payment_result["success"])
        
        # Track conversion
        conversion_result = self.sales_system.track_conversion(
            lead_id=lead_id,
            trial_id=trial_id,
            conversion_type="trial_to_paid",
            amount=299900
        )
        
        self.assertTrue(conversion_result["success"])
        
        # Verify conversion
        lead_details = self.sales_system.get_lead_details(lead_id)
        self.assertEqual(lead_details["status"], "converted")
    
    def test_customer_support_workflow(self):
        """Test customer support workflow"""
        
        # Setup: Create customer
        customer_result = self.customer_system.register_customer(
            email="support@flyfoxai.com",
            name="Support Test",
            password="password123"
        )
        
        customer_id = customer_result["customer_id"]
        
        # Authenticate customer
        auth_result = self.customer_system.authenticate_customer(
            email="support@flyfoxai.com",
            password="password123"
        )
        
        session_token = auth_result["session_token"]
        
        # Validate session
        validation_result = self.customer_system.validate_session_token(session_token)
        
        self.assertTrue(validation_result["success"])
        self.assertEqual(validation_result["customer_id"], customer_id)
        
        # Update customer profile
        update_data = {
            "phone": "+1987654321",
            "company": "Updated Support Corp"
        }
        
        update_result = self.customer_system.update_customer_profile(customer_id, update_data)
        
        self.assertTrue(update_result["success"])
        
        # Verify update
        profile = self.customer_system.get_customer_profile(customer_id)
        self.assertEqual(profile["phone"], "+1987654321")
        self.assertEqual(profile["company"], "Updated Support Corp")
    
    def test_payment_failure_workflow(self):
        """Test payment failure handling workflow"""
        
        # Setup: Create lead and customer
        lead_result = self.sales_system.capture_lead(
            email="payment_fail@flyfoxai.com",
            name="Payment Fail Test",
            company="Payment Fail Corp"
        )
        
        lead_id = lead_result["lead_id"]
        
        customer_result = self.customer_system.register_customer(
            email="payment_fail@flyfoxai.com",
            name="Payment Fail Test",
            password="password123"
        )
        
        customer_id = customer_result["customer_id"]
        
        # Attempt payment with failure
        with patch('stripe.PaymentIntent.create') as mock_payment:
            mock_payment.side_effect = Exception("Payment failed")
            
            payment_result = self.payment_system.process_payment(
                amount=299900,
                currency="usd",
                customer_id=customer_id
            )
            
            self.assertFalse(payment_result["success"])
            self.assertIn("error", payment_result)
        
        # Verify lead status remains as trial
        lead_details = self.sales_system.get_lead_details(lead_id)
        self.assertEqual(lead_details["status"], "trial")
    
    def test_data_consistency_across_systems(self):
        """Test data consistency across all systems"""
        
        # Create customer in both systems
        email = "consistency@flyfoxai.com"
        name = "Consistency Test"
        company = "Consistency Corp"
        
        # Sales system
        lead_result = self.sales_system.capture_lead(
            email=email,
            name=name,
            company=company
        )
        
        # Customer system
        customer_result = self.customer_system.register_customer(
            email=email,
            name=name,
            password="password123"
        )
        
        # Verify data consistency
        lead_details = self.sales_system.get_lead_details(lead_result["lead_id"])
        customer_profile = self.customer_system.get_customer_profile(customer_result["customer_id"])
        
        self.assertEqual(lead_details["email"], customer_profile["email"])
        self.assertEqual(lead_details["name"], customer_profile["name"])
        self.assertEqual(lead_details["company"], company)


class TestSystemIntegration(unittest.TestCase):
    """Test integration between different systems"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_sales_db = tempfile.NamedTemporaryFile(delete=False, suffix='_sales.db')
        self.temp_sales_db.close()
        
        self.temp_customer_db = tempfile.NamedTemporaryFile(delete=False, suffix='_customer.db')
        self.temp_customer_db.close()
        
        self.sales_system = FlyfoxSalesFunnel(db_path=self.temp_sales_db.name)
        self.customer_system = FlyfoxCustomerManagement(db_path=self.temp_customer_db.name)
        self.payment_system = FlyfoxPaymentSystem()
    
    def tearDown(self):
        """Clean up after tests"""
        for db_path in [self.temp_sales_db.name, self.temp_customer_db.name]:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_sales_customer_integration(self):
        """Test integration between sales and customer systems"""
        
        # Create lead in sales system
        lead_result = self.sales_system.capture_lead(
            email="integration@flyfoxai.com",
            name="Integration Test",
            company="Integration Corp"
        )
        
        # Register customer in customer system
        customer_result = self.customer_system.register_customer(
            email="integration@flyfoxai.com",
            name="Integration Test",
            password="password123"
        )
        
        # Verify both systems have consistent data
        lead_details = self.sales_system.get_lead_details(lead_result["lead_id"])
        customer_profile = self.customer_system.get_customer_profile(customer_result["customer_id"])
        
        self.assertEqual(lead_details["email"], customer_profile["email"])
        self.assertEqual(lead_details["name"], customer_profile["name"])
    
    def test_payment_customer_integration(self):
        """Test integration between payment and customer systems"""
        
        # Create customer
        customer_result = self.customer_system.register_customer(
            email="payment_integration@flyfoxai.com",
            name="Payment Integration Test",
            password="password123"
        )
        
        customer_id = customer_result["customer_id"]
        
        # Process payment
        with patch('stripe.Customer.create') as mock_customer:
            mock_customer.return_value = Mock(id="cus_test_integration")
            
            with patch('stripe.PaymentIntent.create') as mock_payment:
                mock_payment.return_value = Mock(
                    id="pi_test_integration",
                    amount=299900,
                    currency="usd",
                    status="succeeded"
                )
                
                payment_result = self.payment_system.process_payment(
                    amount=299900,
                    currency="usd",
                    customer_id=customer_id
                )
                
                self.assertTrue(payment_result["success"])
        
        # Verify customer profile is updated
        customer_profile = self.customer_system.get_customer_profile(customer_id)
        self.assertIsNotNone(customer_profile)
    
    def test_error_propagation_across_systems(self):
        """Test error handling and propagation across systems"""
        
        # Test invalid customer ID in payment system
        with patch('stripe.PaymentIntent.create') as mock_payment:
            mock_payment.side_effect = Exception("Customer not found")
            
            payment_result = self.payment_system.process_payment(
                amount=299900,
                currency="usd",
                customer_id="invalid_customer_id"
            )
            
            self.assertFalse(payment_result["success"])
            self.assertIn("error", payment_result)
        
        # Test invalid lead ID in sales system
        lead_details = self.sales_system.get_lead_details("invalid_lead_id")
        self.assertFalse(lead_details["success"])
        self.assertIn("error", lead_details)
        
        # Test invalid customer ID in customer system
        customer_profile = self.customer_system.get_customer_profile("invalid_customer_id")
        self.assertFalse(customer_profile["success"])
        self.assertIn("error", customer_profile)


class TestPerformanceAndScalability(unittest.TestCase):
    """Test performance and scalability aspects"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_sales_db = tempfile.NamedTemporaryFile(delete=False, suffix='_sales.db')
        self.temp_sales_db.close()
        
        self.temp_customer_db = tempfile.NamedTemporaryFile(delete=False, suffix='_customer.db')
        self.temp_customer_db.close()
        
        self.sales_system = FlyfoxSalesFunnel(db_path=self.temp_sales_db.name)
        self.customer_system = FlyfoxCustomerManagement(db_path=self.temp_customer_db.name)
        self.payment_system = FlyfoxPaymentSystem()
    
    def tearDown(self):
        """Clean up after tests"""
        for db_path in [self.temp_sales_db.name, self.temp_customer_db.name]:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_bulk_lead_processing(self):
        """Test processing multiple leads efficiently"""
        
        # Create 100 leads
        lead_ids = []
        start_time = datetime.now()
        
        for i in range(100):
            result = self.sales_system.capture_lead(
                email=f"bulk_test_{i}@flyfoxai.com",
                name=f"Bulk Test {i}",
                company=f"Bulk Corp {i}"
            )
            
            self.assertTrue(result["success"])
            lead_ids.append(result["lead_id"])
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Should process 100 leads in under 10 seconds
        self.assertLess(processing_time, 10.0)
        self.assertEqual(len(lead_ids), 100)
        
        print(f"✅ Processed 100 leads in {processing_time:.2f} seconds")
    
    def test_concurrent_operations(self):
        """Test concurrent operations across systems"""
        
        import threading
        import time
        
        results = []
        errors = []
        
        def create_customer_thread(thread_id):
            try:
                # Create lead
                lead_result = self.sales_system.capture_lead(
                    email=f"concurrent_{thread_id}@flyfoxai.com",
                    name=f"Concurrent Test {thread_id}",
                    company=f"Concurrent Corp {thread_id}"
                )
                
                # Register customer
                customer_result = self.customer_system.register_customer(
                    email=f"concurrent_{thread_id}@flyfoxai.com",
                    name=f"Concurrent Test {thread_id}",
                    password="password123"
                )
                
                results.append({
                    "thread_id": thread_id,
                    "lead_id": lead_result["lead_id"],
                    "customer_id": customer_result["customer_id"]
                })
                
            except Exception as e:
                errors.append({"thread_id": thread_id, "error": str(e)})
        
        # Start 10 concurrent threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=create_customer_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify results
        self.assertEqual(len(results), 10)
        self.assertEqual(len(errors), 0)
        
        print(f"✅ Successfully processed {len(results)} concurrent operations")
    
    def test_database_performance(self):
        """Test database performance under load"""
        
        # Create 1000 leads and measure performance
        start_time = datetime.now()
        
        for i in range(1000):
            self.sales_system.capture_lead(
                email=f"perf_test_{i}@flyfoxai.com",
                name=f"Performance Test {i}",
                company=f"Performance Corp {i}"
            )
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Should process 1000 leads in under 30 seconds
        self.assertLess(processing_time, 30.0)
        
        # Test query performance
        query_start = datetime.now()
        analytics = self.sales_system.get_conversion_analytics()
        query_end = datetime.now()
        query_time = (query_end - query_start).total_seconds()
        
        # Analytics query should complete in under 1 second
        self.assertLess(query_time, 1.0)
        
        print(f"✅ Created 1000 leads in {processing_time:.2f} seconds")
        print(f"✅ Analytics query completed in {query_time:.3f} seconds")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
