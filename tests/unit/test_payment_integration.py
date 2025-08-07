"""
Unit tests for FLYFOX AI Payment Integration System
Tests Stripe and PayPal payment processing functionality
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from flyfox_payment_integration import FlyfoxPaymentSystem


class TestFlyfoxPaymentSystem(unittest.TestCase):
    """Test cases for FlyfoxPaymentSystem"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.payment_system = FlyfoxPaymentSystem()
        self.test_customer_data = {
            "email": "test@flyfoxai.com",
            "name": "Test User",
            "phone": "+1234567890"
        }
        self.test_payment_data = {
            "amount": 299900,  # $299.99 in cents
            "currency": "usd",
            "description": "FLYFOX AI Professional Plan"
        }
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up any test files or databases
        pass
    
    def test_payment_system_initialization(self):
        """Test that payment system initializes correctly"""
        self.assertIsNotNone(self.payment_system)
        self.assertIsNotNone(self.payment_system.stripe_config)
        self.assertIsNotNone(self.payment_system.paypal_config)
    
    @patch('stripe.Customer.create')
    def test_create_customer_success(self, mock_stripe_customer):
        """Test successful customer creation"""
        # Mock Stripe response
        mock_stripe_customer.return_value = Mock(
            id="cus_test123",
            email="test@flyfoxai.com",
            name="Test User"
        )
        
        result = self.payment_system.create_customer(
            self.test_customer_data["email"],
            self.test_customer_data["name"]
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["customer_id"], "cus_test123")
        self.assertEqual(result["email"], "test@flyfoxai.com")
    
    @patch('stripe.Customer.create')
    def test_create_customer_failure(self, mock_stripe_customer):
        """Test customer creation failure"""
        # Mock Stripe error
        mock_stripe_customer.side_effect = Exception("Stripe API error")
        
        result = self.payment_system.create_customer(
            self.test_customer_data["email"],
            self.test_customer_data["name"]
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    @patch('stripe.PaymentIntent.create')
    def test_process_payment_success(self, mock_payment_intent):
        """Test successful payment processing"""
        # Mock Stripe response
        mock_payment_intent.return_value = Mock(
            id="pi_test123",
            amount=299900,
            currency="usd",
            status="succeeded"
        )
        
        result = self.payment_system.process_payment(
            amount=self.test_payment_data["amount"],
            currency=self.test_payment_data["currency"],
            customer_id="cus_test123"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["payment_id"], "pi_test123")
        self.assertEqual(result["amount"], 299900)
    
    @patch('stripe.PaymentIntent.create')
    def test_process_payment_failure(self, mock_payment_intent):
        """Test payment processing failure"""
        # Mock Stripe error
        mock_payment_intent.side_effect = Exception("Payment failed")
        
        result = self.payment_system.process_payment(
            amount=self.test_payment_data["amount"],
            currency=self.test_payment_data["currency"],
            customer_id="cus_test123"
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_validate_payment_amount(self):
        """Test payment amount validation"""
        # Valid amounts
        self.assertTrue(self.payment_system.validate_payment_amount(1000))  # $10.00
        self.assertTrue(self.payment_system.validate_payment_amount(299900))  # $299.99
        
        # Invalid amounts
        self.assertFalse(self.payment_system.validate_payment_amount(0))
        self.assertFalse(self.payment_system.validate_payment_amount(-100))
        self.assertFalse(self.payment_system.validate_payment_amount(999999999))  # Too large
    
    def test_validate_currency(self):
        """Test currency validation"""
        # Valid currencies
        self.assertTrue(self.payment_system.validate_currency("usd"))
        self.assertTrue(self.payment_system.validate_currency("eur"))
        
        # Invalid currencies
        self.assertFalse(self.payment_system.validate_currency("invalid"))
        self.assertFalse(self.payment_system.validate_currency(""))
    
    def test_validate_email(self):
        """Test email validation"""
        # Valid emails
        self.assertTrue(self.payment_system.validate_email("test@flyfoxai.com"))
        self.assertTrue(self.payment_system.validate_email("user@example.com"))
        
        # Invalid emails
        self.assertFalse(self.payment_system.validate_email("invalid-email"))
        self.assertFalse(self.payment_system.validate_email("@example.com"))
        self.assertFalse(self.payment_system.validate_email(""))
    
    @patch('stripe.Subscription.create')
    def test_create_subscription_success(self, mock_subscription):
        """Test successful subscription creation"""
        # Mock Stripe response
        mock_subscription.return_value = Mock(
            id="sub_test123",
            status="active",
            current_period_end=1234567890
        )
        
        result = self.payment_system.create_subscription(
            customer_id="cus_test123",
            price_id="price_test123"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["subscription_id"], "sub_test123")
        self.assertEqual(result["status"], "active")
    
    @patch('stripe.Subscription.create')
    def test_create_subscription_failure(self, mock_subscription):
        """Test subscription creation failure"""
        # Mock Stripe error
        mock_subscription.side_effect = Exception("Subscription failed")
        
        result = self.payment_system.create_subscription(
            customer_id="cus_test123",
            price_id="price_test123"
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_generate_payment_link(self):
        """Test payment link generation"""
        result = self.payment_system.generate_payment_link(
            amount=self.test_payment_data["amount"],
            currency=self.test_payment_data["currency"],
            description=self.test_payment_data["description"]
        )
        
        self.assertTrue(result["success"])
        self.assertIn("payment_link", result)
        self.assertIsInstance(result["payment_link"], str)
    
    def test_refund_payment(self):
        """Test payment refund functionality"""
        # This would need to be implemented in the actual system
        # For now, we'll test the method exists
        self.assertTrue(hasattr(self.payment_system, 'refund_payment'))
    
    def test_get_payment_history(self):
        """Test payment history retrieval"""
        # This would need to be implemented in the actual system
        # For now, we'll test the method exists
        self.assertTrue(hasattr(self.payment_system, 'get_payment_history'))


class TestPayPalIntegration(unittest.TestCase):
    """Test cases for PayPal integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.payment_system = FlyfoxPaymentSystem()
    
    @patch('paypalrestsdk.Payment')
    def test_paypal_payment_creation(self, mock_paypal_payment):
        """Test PayPal payment creation"""
        # Mock PayPal response
        mock_paypal_payment.return_value = Mock(
            id="PAY-123456789",
            state="created",
            links=[{"href": "https://www.sandbox.paypal.com/cgi-bin/webscr"}]
        )
        
        result = self.payment_system.create_paypal_payment(
            amount=299900,
            currency="usd",
            description="FLYFOX AI Professional Plan"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("payment_id", result)
        self.assertIn("approval_url", result)


class TestSecurityFeatures(unittest.TestCase):
    """Test cases for security features"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.payment_system = FlyfoxPaymentSystem()
    
    def test_api_key_validation(self):
        """Test API key validation"""
        # Test that API keys are properly configured
        self.assertIsNotNone(self.payment_system.stripe_config.get("secret_key"))
        self.assertIsNotNone(self.payment_system.paypal_config.get("client_id"))
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        # Test that inputs are properly sanitized
        test_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE customers; --",
            "normal@email.com"
        ]
        
        for test_input in test_inputs:
            sanitized = self.payment_system.sanitize_input(test_input)
            self.assertNotIn("<script>", sanitized)
            self.assertNotIn("DROP TABLE", sanitized)
    
    def test_payment_data_encryption(self):
        """Test payment data encryption"""
        # Test that sensitive data is encrypted
        test_data = {"card_number": "4242424242424242"}
        encrypted = self.payment_system.encrypt_sensitive_data(test_data)
        
        self.assertNotEqual(test_data["card_number"], encrypted["card_number"])
        self.assertIsInstance(encrypted["card_number"], str)


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.payment_system = FlyfoxPaymentSystem()
    
    def test_network_error_handling(self):
        """Test network error handling"""
        with patch('stripe.Customer.create') as mock_create:
            mock_create.side_effect = Exception("Network error")
            
            result = self.payment_system.create_customer("test@example.com", "Test User")
            
            self.assertFalse(result["success"])
            self.assertIn("error", result)
            self.assertIn("Network error", str(result["error"]))
    
    def test_invalid_data_handling(self):
        """Test invalid data handling"""
        # Test with invalid email
        result = self.payment_system.create_customer("invalid-email", "Test User")
        self.assertFalse(result["success"])
        
        # Test with invalid amount
        result = self.payment_system.process_payment(amount=-100, currency="usd")
        self.assertFalse(result["success"])
    
    def test_rate_limiting_handling(self):
        """Test rate limiting error handling"""
        with patch('stripe.Customer.create') as mock_create:
            mock_create.side_effect = Exception("Rate limit exceeded")
            
            result = self.payment_system.create_customer("test@example.com", "Test User")
            
            self.assertFalse(result["success"])
            self.assertIn("error", result)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
