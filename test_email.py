#!/usr/bin/env python3
"""
Send a test alert email to verify email configuration
Run this to test your email settings before deployment
"""

import sys
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from email_sender import EmailSender
from performance_visualizer import PerformanceVisualizer
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

print("=" * 60)
print("GrowattAlert - Email Test Script")
print("=" * 60)
print()

try:
    # Initialize email sender
    print("📧 Initializing email sender...")
    sender = EmailSender()
    
    # Test SMTP connection
    print("🔌 Testing SMTP connection...")
    if sender.test_connection():
        print("✓ SMTP connection successful!")
    else:
        print("✗ SMTP connection failed")
        sys.exit(1)
    
    print()
    response = input("Send a test alert email? (y/n): ")
    
    if response.lower() == 'y':
        print("\n📨 Sending test alert email...")
        
        # Create test data
        test_data = {
            'power': 750,
            'battery_voltage': 48.5,
            'energy_today': 15.3,
            'status': 'Testing'
        }
        
        # Generate test graphs
        visualizer = PerformanceVisualizer()
        times = [datetime.now()]
        powers = [750]
        voltages = [48.5]
        
        graphs = {
            'power_graph': visualizer.create_power_graph(times, powers, 709),
            'voltage_graph': visualizer.create_voltage_graph(times, voltages, 51),
            'dashboard': visualizer.create_dashboard(test_data)
        }
        
        # Send test alert
        success = sender.send_alert_email('power', test_data, graphs)
        
        if success:
            print("\n✓ Test email sent successfully!")
            print("  Check your inbox for the test alert.")
        else:
            print("\n✗ Failed to send test email")
            print("  Check logs for details")
    else:
        print("\nTest skipped.")
    
    print("\n" + "=" * 60)
    print("Email configuration test complete!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
