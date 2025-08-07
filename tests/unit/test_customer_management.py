"""
Unit tests for FLYFOX AI Customer Management System
Tests customer registration, authentication, and data management
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
import sqlite3

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from flyfox_customer_management import FlyfoxCustomerManagement


class TestFlyfoxCustomerManagement(unittest.TestCase):
    """Test cases for FlyfoxCustomerManagement"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.customer_system = FlyfoxCustomerManagement(db_path=self.temp_db.name)
        self.test_customer_data = {
            "email": "test@flyfoxai.com",
            "name": "Test User",
            "password": "secure_password_123",
            "phone": "+1234567890",
            "company": "Test Corp"
        }
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove temporary database
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_customer_system_initialization(self):
        """Test that customer system initializes correctly"""
        self.assertIsNotNone(self.customer_system)
        self.assertIsNotNone(self.customer_system.db_path)
        
        # Check that database tables are created
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            self.assertIn("customers", tables)
            self.assertIn("customer_sessions", tables)
    
    def test_register_customer_success(self):
        """Test successful customer registration"""
        result = self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        self.assertTrue(result["success"])
        self.assertIn("customer_id", result)
        self.assertEqual(result["email"], self.test_customer_data["email"])
        self.assertEqual(result["name"], self.test_customer_data["name"])
    
    def test_register_customer_duplicate_email(self):
        """Test customer registration with duplicate email"""
        # Register first customer
        result1 = self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        self.assertTrue(result1["success"])
        
        # Try to register with same email
        result2 = self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name="Another User",
            password="another_password"
        )
        
        self.assertFalse(result2["success"])
        self.assertIn("error", result2)
    
    def test_register_customer_invalid_email(self):
        """Test customer registration with invalid email"""
        result = self.customer_system.register_customer(
            email="invalid-email",
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_register_customer_weak_password(self):
        """Test customer registration with weak password"""
        result = self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password="123"  # Too short
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_authenticate_customer_success(self):
        """Test successful customer authentication"""
        # First register a customer
        self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        # Then authenticate
        result = self.customer_system.authenticate_customer(
            email=self.test_customer_data["email"],
            password=self.test_customer_data["password"]
        )
        
        self.assertTrue(result["success"])
        self.assertIn("session_token", result)
        self.assertIn("customer_id", result)
    
    def test_authenticate_customer_invalid_credentials(self):
        """Test customer authentication with invalid credentials"""
        # First register a customer
        self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        # Try to authenticate with wrong password
        result = self.customer_system.authenticate_customer(
            email=self.test_customer_data["email"],
            password="wrong_password"
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_authenticate_customer_nonexistent(self):
        """Test authentication for non-existent customer"""
        result = self.customer_system.authenticate_customer(
            email="nonexistent@example.com",
            password="any_password"
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_get_customer_profile(self):
        """Test retrieving customer profile"""
        # First register a customer
        register_result = self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        customer_id = register_result["customer_id"]
        
        # Get customer profile
        result = self.customer_system.get_customer_profile(customer_id)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["email"], self.test_customer_data["email"])
        self.assertEqual(result["name"], self.test_customer_data["name"])
        self.assertNotIn("password", result)  # Password should not be returned
    
    def test_update_customer_profile(self):
        """Test updating customer profile"""
        # First register a customer
        register_result = self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        customer_id = register_result["customer_id"]
        
        # Update customer profile
        update_data = {
            "name": "Updated Name",
            "phone": "+1987654321",
            "company": "Updated Corp"
        }
        
        result = self.customer_system.update_customer_profile(customer_id, update_data)
        
        self.assertTrue(result["success"])
        
        # Verify the update
        profile = self.customer_system.get_customer_profile(customer_id)
        self.assertEqual(profile["name"], "Updated Name")
        self.assertEqual(profile["phone"], "+1987654321")
        self.assertEqual(profile["company"], "Updated Corp")
    
    def test_delete_customer(self):
        """Test customer deletion"""
        # First register a customer
        register_result = self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        customer_id = register_result["customer_id"]
        
        # Delete customer
        result = self.customer_system.delete_customer(customer_id)
        
        self.assertTrue(result["success"])
        
        # Verify customer is deleted
        profile = self.customer_system.get_customer_profile(customer_id)
        self.assertFalse(profile["success"])
    
    def test_password_reset(self):
        """Test password reset functionality"""
        # First register a customer
        self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        # Request password reset
        result = self.customer_system.request_password_reset(
            email=self.test_customer_data["email"]
        )
        
        self.assertTrue(result["success"])
        self.assertIn("reset_token", result)
    
    def test_password_reset_nonexistent_email(self):
        """Test password reset for non-existent email"""
        result = self.customer_system.request_password_reset(
            email="nonexistent@example.com"
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_validate_session_token(self):
        """Test session token validation"""
        # First register and authenticate a customer
        self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        auth_result = self.customer_system.authenticate_customer(
            email=self.test_customer_data["email"],
            password=self.test_customer_data["password"]
        )
        
        session_token = auth_result["session_token"]
        
        # Validate session token
        result = self.customer_system.validate_session_token(session_token)
        
        self.assertTrue(result["success"])
        self.assertIn("customer_id", result)
    
    def test_validate_session_token_invalid(self):
        """Test session token validation with invalid token"""
        result = self.customer_system.validate_session_token("invalid_token")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_logout_customer(self):
        """Test customer logout"""
        # First register and authenticate a customer
        self.customer_system.register_customer(
            email=self.test_customer_data["email"],
            name=self.test_customer_data["name"],
            password=self.test_customer_data["password"]
        )
        
        auth_result = self.customer_system.authenticate_customer(
            email=self.test_customer_data["email"],
            password=self.test_customer_data["password"]
        )
        
        session_token = auth_result["session_token"]
        
        # Logout customer
        result = self.customer_system.logout_customer(session_token)
        
        self.assertTrue(result["success"])
        
        # Verify session is invalidated
        validation_result = self.customer_system.validate_session_token(session_token)
        self.assertFalse(validation_result["success"])


class TestDataValidation(unittest.TestCase):
    """Test cases for data validation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.customer_system = FlyfoxCustomerManagement(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_validate_email(self):
        """Test email validation"""
        # Valid emails
        self.assertTrue(self.customer_system.validate_email("test@flyfoxai.com"))
        self.assertTrue(self.customer_system.validate_email("user@example.com"))
        self.assertTrue(self.customer_system.validate_email("user+tag@example.com"))
        
        # Invalid emails
        self.assertFalse(self.customer_system.validate_email("invalid-email"))
        self.assertFalse(self.customer_system.validate_email("@example.com"))
        self.assertFalse(self.customer_system.validate_email("user@"))
        self.assertFalse(self.customer_system.validate_email(""))
    
    def test_validate_password(self):
        """Test password validation"""
        # Valid passwords
        self.assertTrue(self.customer_system.validate_password("SecurePass123!"))
        self.assertTrue(self.customer_system.validate_password("MyPassword123"))
        
        # Invalid passwords (too short)
        self.assertFalse(self.customer_system.validate_password("123"))
        self.assertFalse(self.customer_system.validate_password("short"))
        
        # Invalid passwords (no numbers)
        self.assertFalse(self.customer_system.validate_password("NoNumbers"))
        
        # Invalid passwords (no letters)
        self.assertFalse(self.customer_system.validate_password("123456789"))
    
    def test_validate_phone(self):
        """Test phone number validation"""
        # Valid phone numbers
        self.assertTrue(self.customer_system.validate_phone("+1234567890"))
        self.assertTrue(self.customer_system.validate_phone("123-456-7890"))
        self.assertTrue(self.customer_system.validate_phone("(123) 456-7890"))
        
        # Invalid phone numbers
        self.assertFalse(self.customer_system.validate_phone("123"))
        self.assertFalse(self.customer_system.validate_phone("not-a-phone"))
        self.assertFalse(self.customer_system.validate_phone(""))


class TestSecurityFeatures(unittest.TestCase):
    """Test cases for security features"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.customer_system = FlyfoxCustomerManagement(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed"""
        # Register a customer
        self.customer_system.register_customer(
            email="test@example.com",
            name="Test User",
            password="my_password_123"
        )
        
        # Check that password is hashed in database
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM customers WHERE email = ?", ("test@example.com",))
            stored_password = cursor.fetchone()[0]
            
            # Password should be hashed, not plain text
            self.assertNotEqual(stored_password, "my_password_123")
            self.assertTrue(len(stored_password) > 20)  # Hash should be longer than plain text
    
    def test_session_token_security(self):
        """Test session token security"""
        # Register and authenticate a customer
        self.customer_system.register_customer(
            email="test@example.com",
            name="Test User",
            password="my_password_123"
        )
        
        auth_result = self.customer_system.authenticate_customer(
            email="test@example.com",
            password="my_password_123"
        )
        
        session_token = auth_result["session_token"]
        
        # Session token should be secure
        self.assertIsInstance(session_token, str)
        self.assertTrue(len(session_token) > 32)  # Should be a long, secure token
    
    def test_sql_injection_protection(self):
        """Test SQL injection protection"""
        # Try to register with SQL injection attempt
        result = self.customer_system.register_customer(
            email="test@example.com'; DROP TABLE customers; --",
            name="Test User",
            password="my_password_123"
        )
        
        # Should handle gracefully (either reject or escape)
        # The important thing is that it doesn't crash or execute the injection
        self.assertIsInstance(result, dict)
        
        # Check that customers table still exists
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
            table_exists = cursor.fetchone() is not None
            self.assertTrue(table_exists)


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.customer_system = FlyfoxCustomerManagement(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_database_connection_error(self):
        """Test handling of database connection errors"""
        # Create customer system with invalid database path
        invalid_system = FlyfoxCustomerManagement(db_path="/invalid/path/db.sqlite")
        
        result = invalid_system.register_customer(
            email="test@example.com",
            name="Test User",
            password="my_password_123"
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_invalid_customer_id(self):
        """Test handling of invalid customer ID"""
        result = self.customer_system.get_customer_profile("invalid_id")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_malformed_data(self):
        """Test handling of malformed data"""
        # Test with None values
        result = self.customer_system.register_customer(
            email=None,
            name=None,
            password=None
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
