#!/usr/bin/env python3
"""
FLYFOX AI - Payment Integration System
Complete payment processing and subscription management
"""

import stripe
import paypalrestsdk
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlyfoxPaymentSystem:
    """FLYFOX AI Complete Payment Processing System"""
    
    def __init__(self):
        # Initialize payment providers
        self.stripe = stripe
        self.paypal = paypalrestsdk
        
        # FLYFOX AI Pricing Tiers
        self.pricing_tiers = {
            "quantum_starter": {
                "name": "Quantum Starter",
                "price": 2999,  # $2,999/month
                "stripe_price_id": "price_quantum_starter",
                "paypal_plan_id": "P-QUANTUM-STARTER",
                "features": [
                    "1,000 quantum-enhanced voice calls/month",
                    "Basic quantum AI responses",
                    "Standard voice quality",
                    "Email support",
                    "FLYFOX AI branding"
                ]
            },
            "quantum_professional": {
                "name": "Quantum Professional", 
                "price": 7999,  # $7,999/month
                "stripe_price_id": "price_quantum_professional",
                "paypal_plan_id": "P-QUANTUM-PROFESSIONAL",
                "features": [
                    "5,000 quantum-enhanced voice calls/month",
                    "Advanced qdLLM responses",
                    "Quantum NLP understanding",
                    "Bidirectional reasoning",
                    "Priority support",
                    "Custom FLYFOX AI branding"
                ]
            },
            "quantum_enterprise": {
                "name": "Quantum Enterprise",
                "price": 19999,  # $19,999/month
                "stripe_price_id": "price_quantum_enterprise", 
                "paypal_plan_id": "P-QUANTUM-ENTERPRISE",
                "features": [
                    "Unlimited quantum-enhanced voice calls",
                    "Full quantum AI capabilities",
                    "Custom quantum model training",
                    "Dedicated support team",
                    "White-label options",
                    "Advanced integrations"
                ]
            },
            "quantum_elite": {
                "name": "Quantum Elite",
                "price": 49999,  # $49,999/month
                "stripe_price_id": "price_quantum_elite",
                "paypal_plan_id": "P-QUANTUM-ELITE", 
                "features": [
                    "Unlimited + custom quantum processing",
                    "Custom quantum AI development",
                    "Proprietary quantum algorithms",
                    "Dedicated quantum computing resources",
                    "Custom integrations",
                    "White-label platform"
                ]
            }
        }
        
        # Initialize payment providers
        self._setup_payment_providers()
    
    def _setup_payment_providers(self):
        """Setup Stripe and PayPal configurations"""
        try:
            # Stripe configuration
            stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
            
            # PayPal configuration
            paypalrestsdk.configure({
                "mode": os.getenv("PAYPAL_MODE", "sandbox"),  # sandbox or live
                "client_id": os.getenv("PAYPAL_CLIENT_ID", ""),
                "client_secret": os.getenv("PAYPAL_CLIENT_SECRET", "")
            })
            
            logger.info("✅ Payment providers configured successfully")
            
        except Exception as e:
            logger.error(f"❌ Payment provider setup failed: {e}")
    
    def create_customer(self, email: str, name: str, company: str = None) -> Dict:
        """Create a new FLYFOX AI customer"""
        try:
            # Create Stripe customer
            stripe_customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    "company": company or "",
                    "platform": "FLYFOX AI",
                    "created_at": datetime.now().isoformat()
                }
            )
            
            # Create customer record
            customer_data = {
                "customer_id": stripe_customer.id,
                "email": email,
                "name": name,
                "company": company,
                "subscription_status": "inactive",
                "created_at": datetime.now().isoformat(),
                "platform": "FLYFOX AI"
            }
            
            logger.info(f"✅ Customer created: {email}")
            return customer_data
            
        except Exception as e:
            logger.error(f"❌ Customer creation failed: {e}")
            return {"error": str(e)}
    
    def create_subscription(self, customer_id: str, tier: str, payment_method: str = "stripe") -> Dict:
        """Create a FLYFOX AI subscription"""
        try:
            tier_data = self.pricing_tiers.get(tier)
            if not tier_data:
                return {"error": "Invalid tier specified"}
            
            if payment_method == "stripe":
                return self._create_stripe_subscription(customer_id, tier, tier_data)
            elif payment_method == "paypal":
                return self._create_paypal_subscription(customer_id, tier, tier_data)
            else:
                return {"error": "Unsupported payment method"}
                
        except Exception as e:
            logger.error(f"❌ Subscription creation failed: {e}")
            return {"error": str(e)}
    
    def _create_stripe_subscription(self, customer_id: str, tier: str, tier_data: Dict) -> Dict:
        """Create Stripe subscription"""
        try:
            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": tier_data["stripe_price_id"]}],
                metadata={
                    "tier": tier,
                    "platform": "FLYFOX AI",
                    "features": json.dumps(tier_data["features"])
                }
            )
            
            subscription_data = {
                "subscription_id": subscription.id,
                "customer_id": customer_id,
                "tier": tier,
                "status": subscription.status,
                "current_period_start": datetime.fromtimestamp(subscription.current_period_start),
                "current_period_end": datetime.fromtimestamp(subscription.current_period_end),
                "amount": tier_data["price"],
                "currency": "usd",
                "payment_method": "stripe",
                "features": tier_data["features"]
            }
            
            logger.info(f"✅ Stripe subscription created: {subscription.id}")
            return subscription_data
            
        except Exception as e:
            logger.error(f"❌ Stripe subscription creation failed: {e}")
            return {"error": str(e)}
    
    def _create_paypal_subscription(self, customer_id: str, tier: str, tier_data: Dict) -> Dict:
        """Create PayPal subscription"""
        try:
            # Create PayPal billing plan
            billing_plan = paypalrestsdk.BillingPlan({
                "name": f"FLYFOX AI {tier_data['name']}",
                "description": f"FLYFOX AI {tier_data['name']} subscription",
                "type": "FIXED",
                "payment_definitions": [{
                    "name": "Regular Payments",
                    "type": "REGULAR",
                    "frequency": "MONTH",
                    "frequency_interval": "1",
                    "amount": {
                        "value": str(tier_data["price"]),
                        "currency": "USD"
                    }
                }],
                "merchant_preferences": {
                    "setup_fee": {
                        "value": "0",
                        "currency": "USD"
                    },
                    "return_url": "https://flyfoxai.com/success",
                    "cancel_url": "https://flyfoxai.com/cancel",
                    "auto_bill_amount": "YES",
                    "initial_fail_amount_action": "CONTINUE",
                    "max_fail_attempts": "0"
                }
            })
            
            if billing_plan.create():
                subscription_data = {
                    "subscription_id": billing_plan.id,
                    "customer_id": customer_id,
                    "tier": tier,
                    "status": "active",
                    "amount": tier_data["price"],
                    "currency": "usd",
                    "payment_method": "paypal",
                    "features": tier_data["features"]
                }
                
                logger.info(f"✅ PayPal subscription created: {billing_plan.id}")
                return subscription_data
            else:
                return {"error": "PayPal subscription creation failed"}
                
        except Exception as e:
            logger.error(f"❌ PayPal subscription creation failed: {e}")
            return {"error": str(e)}
    
    def process_payment(self, amount: int, currency: str = "usd", payment_method: str = "stripe") -> Dict:
        """Process a one-time payment"""
        try:
            if payment_method == "stripe":
                return self._process_stripe_payment(amount, currency)
            elif payment_method == "paypal":
                return self._process_paypal_payment(amount, currency)
            else:
                return {"error": "Unsupported payment method"}
                
        except Exception as e:
            logger.error(f"❌ Payment processing failed: {e}")
            return {"error": str(e)}
    
    def _process_stripe_payment(self, amount: int, currency: str) -> Dict:
        """Process Stripe payment"""
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata={
                    "platform": "FLYFOX AI",
                    "payment_type": "one_time"
                }
            )
            
            return {
                "payment_id": payment_intent.id,
                "amount": amount,
                "currency": currency,
                "status": payment_intent.status,
                "client_secret": payment_intent.client_secret
            }
            
        except Exception as e:
            logger.error(f"❌ Stripe payment failed: {e}")
            return {"error": str(e)}
    
    def _process_paypal_payment(self, amount: int, currency: str) -> Dict:
        """Process PayPal payment"""
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": str(amount / 100),  # Convert cents to dollars
                        "currency": currency.upper()
                    },
                    "description": "FLYFOX AI Quantum Voice Platform"
                }],
                "redirect_urls": {
                    "return_url": "https://flyfoxai.com/success",
                    "cancel_url": "https://flyfoxai.com/cancel"
                }
            })
            
            if payment.create():
                return {
                    "payment_id": payment.id,
                    "amount": amount,
                    "currency": currency,
                    "status": payment.state,
                    "approval_url": payment.links[1].href
                }
            else:
                return {"error": "PayPal payment creation failed"}
                
        except Exception as e:
            logger.error(f"❌ PayPal payment failed: {e}")
            return {"error": str(e)}
    
    def generate_invoice(self, customer_id: str, subscription_id: str, amount: int) -> Dict:
        """Generate invoice for FLYFOX AI subscription"""
        try:
            invoice = stripe.Invoice.create(
                customer=customer_id,
                subscription=subscription_id,
                metadata={
                    "platform": "FLYFOX AI",
                    "invoice_type": "subscription"
                }
            )
            
            invoice_data = {
                "invoice_id": invoice.id,
                "customer_id": customer_id,
                "subscription_id": subscription_id,
                "amount": amount,
                "currency": "usd",
                "status": invoice.status,
                "hosted_invoice_url": invoice.hosted_invoice_url,
                "invoice_pdf": invoice.invoice_pdf
            }
            
            logger.info(f"✅ Invoice generated: {invoice.id}")
            return invoice_data
            
        except Exception as e:
            logger.error(f"❌ Invoice generation failed: {e}")
            return {"error": str(e)}
    
    def get_subscription_status(self, subscription_id: str) -> Dict:
        """Get subscription status"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_start": datetime.fromtimestamp(subscription.current_period_start),
                "current_period_end": datetime.fromtimestamp(subscription.current_period_end),
                "cancel_at_period_end": subscription.cancel_at_period_end
            }
            
        except Exception as e:
            logger.error(f"❌ Subscription status check failed: {e}")
            return {"error": str(e)}
    
    def cancel_subscription(self, subscription_id: str) -> Dict:
        """Cancel subscription"""
        try:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            
            return {
                "subscription_id": subscription.id,
                "status": "canceling",
                "cancel_at_period_end": True
            }
            
        except Exception as e:
            logger.error(f"❌ Subscription cancellation failed: {e}")
            return {"error": str(e)}

# FLYFOX AI Payment System Demo
def demo_flyfox_payment_system():
    """Demonstrate FLYFOX AI payment system"""
    print("🚀 FLYFOX AI - Payment Integration System Demo")
    print("=" * 50)
    
    # Initialize payment system
    payment_system = FlyfoxPaymentSystem()
    
    # Demo customer creation
    print("\n1. Creating FLYFOX AI customer...")
    customer = payment_system.create_customer(
        email="demo@flyfoxai.com",
        name="Demo Customer",
        company="Demo Corp"
    )
    print(f"✅ Customer created: {customer}")
    
    # Demo subscription creation
    print("\n2. Creating FLYFOX AI subscription...")
    subscription = payment_system.create_subscription(
        customer_id=customer["customer_id"],
        tier="quantum_starter",
        payment_method="stripe"
    )
    print(f"✅ Subscription created: {subscription}")
    
    # Demo payment processing
    print("\n3. Processing FLYFOX AI payment...")
    payment = payment_system.process_payment(
        amount=299900,  # $2,999.00
        currency="usd",
        payment_method="stripe"
    )
    print(f"✅ Payment processed: {payment}")
    
    # Demo invoice generation
    print("\n4. Generating FLYFOX AI invoice...")
    invoice = payment_system.generate_invoice(
        customer_id=customer["customer_id"],
        subscription_id=subscription["subscription_id"],
        amount=299900
    )
    print(f"✅ Invoice generated: {invoice}")
    
    print("\n🎉 FLYFOX AI Payment System Ready for Sales!")
    print("Contact: john.britton@goliathomniedge.com")
    print("Website: https://flyfoxai.com")

if __name__ == "__main__":
    demo_flyfox_payment_system()
