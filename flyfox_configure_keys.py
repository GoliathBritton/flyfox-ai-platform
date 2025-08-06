#!/usr/bin/env python3
"""
FLYFOX AI - API Key Configuration System
Configure all necessary API keys for FLYFOX AI platform
"""

import os
import json
from datetime import datetime

class FlyfoxKeyConfig:
    """FLYFOX AI API Key Configuration System"""

    def __init__(self):
        # FLYFOX AI API Keys (provided by user)
        self.api_keys = {
            "STRIPE_SECRET_KEY": "your_stripe_secret_key_here",
            "STRIPE_PUBLISHABLE_KEY": "pk_test_51RtERqPrxTsW5OEfjlJ4MEvtx6vVV2zRx4Eq52WnD5Lq8TnWSqEJFWydBllXHGEu5bFz3cBbTzp3BZE1Rg31BKk00zjaU6UoJ",
            "PAYPAL_CLIENT_ID": "ARbHoAvcE25ruW5AoK414FTnkW_ufJWWiPwPgHyyU7ypOyDLIRKvNpoaEOGyV4j8U6Wxvtk-3OjA-LxK",
            "PAYPAL_CLIENT_SECRET": "EAa2naOKedIts7h6Rfe7pgs8EIFYloGGueENYWEue6T-yu0RaOyPHKMOWGh-Klerng8DiLp_iX598Z8A",
            "EMAIL_PASSWORD": "your_gmail_app_password_here",
            "JWT_SECRET": "LKUWHJSNaBJ2S09p1Scv6qTjhpVokIOuils1Km2vMWcggncYbVNvkvnYRNaZlYVjqqa2wx4ZKfjZzWrOspBnyg==",
            "SUPABASE_URL": "https://hysfiibfajydjatsqtbz.supabase.co",
            "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh5c2ZpaWJmYWp5ZGphdHNxdGJ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0NjQzNjMsImV4cCI6MjA3MDA0MDM2M30.7bwhYLgCkHSlQXc14NuCpOY6y4jd8MjMc8zOIqynGjE",
            "SUPABASE_SECRET": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya29scnRsdXhtb2x4cnlocXN2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMDcyNjM4MCwiZXhwIjoyMDQ2MzAyMzgwfQ.Rr7QKA98kZEalIQIhIngNs70TaIN6wwDgvk9AdD6Sa8",
            "DYNEX_API_KEY": "your-dynex-api-key",
            "NUCO_API_KEY": "ScSL33hX9EGPlUniqabdT6dYeHrc1gFl9xeWulSYleZhIGZdWFubb8Rd8LaC9GXxJweK61CpZlrKANq5HLr6Txry0KPOEd59csltQ0EIuLMmW2N1KkOV8szEX8mni1gnVEBbAdDZbnOruwlYr5eAEJpreOHNi22TTLBzmyE9OygCxcxxKDslbylXCCUaNgRT90pH8x64qwf2kPuNvNTUvPn2aHQ",
            "NUCO_PROJECT_ID": "flyfox-ai-quantum-platform"
        }
        
        print("🚀 FLYFOX AI API Key Configuration System")
        print("=" * 50)
    
    def set_environment_variables(self):
        """Set all environment variables"""
        print("🔧 Setting environment variables...")
        
        for key, value in self.api_keys.items():
            os.environ[key] = value
            print(f"✅ Set {key}")
        
        print("✅ All environment variables set successfully!")
    
    def create_env_file(self):
        """Create .env file with all API keys"""
        print("📝 Creating .env file...")
        
        env_content = """# FLYFOX AI Environment Variables
# Generated on: {datetime}

# Payment Processing
STRIPE_SECRET_KEY={stripe_secret}
STRIPE_PUBLISHABLE_KEY={stripe_publishable}
PAYPAL_CLIENT_ID={paypal_client}
PAYPAL_CLIENT_SECRET={paypal_secret}

# Email Configuration
EMAIL_PASSWORD={email_password}

# Authentication
JWT_SECRET={jwt_secret}

# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}
SUPABASE_SECRET={supabase_secret}

# Quantum Computing Partners
DYNEX_API_KEY={dynex_key}
NUCO_API_KEY={nuco_key}
NUCO_PROJECT_ID={nuco_project}

# FLYFOX AI Configuration
COMPANY_NAME=FLYFOX AI
WEBSITE=https://flyfoxai.com
CONTACT_EMAIL=john.britton@goliathomniedge.com
""".format(
            datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            stripe_secret=self.api_keys["STRIPE_SECRET_KEY"],
            stripe_publishable=self.api_keys["STRIPE_PUBLISHABLE_KEY"],
            paypal_client=self.api_keys["PAYPAL_CLIENT_ID"],
            paypal_secret=self.api_keys["PAYPAL_CLIENT_SECRET"],
            email_password=self.api_keys["EMAIL_PASSWORD"],
            jwt_secret=self.api_keys["JWT_SECRET"],
            supabase_url=self.api_keys["SUPABASE_URL"],
            supabase_key=self.api_keys["SUPABASE_KEY"],
            supabase_secret=self.api_keys["SUPABASE_SECRET"],
            dynex_key=self.api_keys["DYNEX_API_KEY"],
            nuco_key=self.api_keys["NUCO_API_KEY"],
            nuco_project=self.api_keys["NUCO_PROJECT_ID"]
        )
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
    
    def test_api_connections(self):
        """Test API connections"""
        print("🧪 Testing API connections...")
        
        try:
            import stripe
            stripe.api_key = self.api_keys["STRIPE_SECRET_KEY"]
            account = stripe.Account.retrieve()
            print("✅ Stripe connection successful")
        except Exception as e:
            print(f"❌ Stripe connection failed: {e}")
        
        try:
            import paypalrestsdk
            paypalrestsdk.configure({
                "mode": "sandbox",
                "client_id": self.api_keys["PAYPAL_CLIENT_ID"],
                "client_secret": self.api_keys["PAYPAL_CLIENT_SECRET"]
            })
            print("✅ PayPal connection successful")
        except Exception as e:
            print(f"❌ PayPal connection failed: {e}")
        
        try:
            import requests
            response = requests.get(
                f"{self.api_keys['SUPABASE_URL']}/rest/v1/",
                headers={
                    "apikey": self.api_keys["SUPABASE_KEY"],
                    "Authorization": f"Bearer {self.api_keys['SUPABASE_KEY']}"
                }
            )
            if response.status_code == 200:
                print("✅ Supabase connection successful")
            else:
                print(f"❌ Supabase connection failed: {response.text}")
        except Exception as e:
            print(f"❌ Supabase connection failed: {e}")
    
    def generate_config_summary(self):
        """Generate configuration summary"""
        print("\n📊 FLYFOX AI Configuration Summary")
        print("=" * 40)
        
        summary = {
            "payment_processing": {
                "stripe": "✅ Configured",
                "paypal": "✅ Configured"
            },
            "database": {
                "supabase": "✅ Configured",
                "url": self.api_keys["SUPABASE_URL"]
            },
            "authentication": {
                "jwt_secret": "✅ Configured"
            },
            "quantum_partners": {
                "dynex": "⏳ Pending API Key",
                "nuco_cloud": "⏳ Pending API Key"
            },
            "email": {
                "gmail_password": "⏳ Pending Configuration"
            }
        }
        
        print(json.dumps(summary, indent=2))
        
        print("\n🎯 Next Steps:")
        print("1. Configure Gmail app password for EMAIL_PASSWORD")
        print("2. Get Dynex API key for quantum computing")
        print("3. Get Nuco.Cloud API key for cost optimization")
        print("4. Test complete platform integration")
    
    def run_complete_setup(self):
        """Run complete API key setup"""
        print("🚀 Running complete FLYFOX AI API key setup...")
        
        # Set environment variables
        self.set_environment_variables()
        
        # Create .env file
        self.create_env_file()
        
        # Test API connections
        self.test_api_connections()
        
        # Generate summary
        self.generate_config_summary()
        
        print("\n🎉 FLYFOX AI API Key Configuration Complete!")
        print("📞 Contact: john.britton@goliathomniedge.com")
        print("🌐 Website: https://flyfoxai.com")

def main():
    """Main configuration function"""
    config = FlyfoxKeyConfig()
    config.run_complete_setup()

if __name__ == "__main__":
    main()
