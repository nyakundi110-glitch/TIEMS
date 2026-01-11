#!/usr/bin/env python3
"""
Send test alert to specified email addresses
"""

import sys
import json
import logging
from datetime import datetime
from email_sender import EmailSender
from performance_visualizer import PerformanceVisualizer

logging.basicConfig(level=logging.INFO)

print("=" * 70)
print("GrowattAlert - Sending Test Alert")
print("=" * 70)
print()

try:
    # Load base config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Override recipient emails for this test
    config['email']['recipient_emails'] = [
        'nyakundi110@gmail.com',
        'carolinejosphat7@gmail.com'
    ]
    
    print(f"Sender: {config['email']['sender_email']}")
    print(f"Recipients:")
    for email in config['email']['recipient_emails']:
        print(f"  - {email}")
    print()
    
    # Save modified config temporarily
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # Initialize email sender
    print("Initializing email sender...")
    sender = EmailSender()
    
    # Test SMTP connection
    print("Testing SMTP connection...")
    if not sender.test_connection():
        print("[ERROR] SMTP connection failed!")
        sys.exit(1)
    
    print("[OK] SMTP connection successful!")
    print()
    
    # Create test data
    print("Generating test alert data...")
    test_data = {
        'power': 750,
        'battery_voltage': 48.5,
        'energy_today': 15.3,
        'status': 'Testing Alert System',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Generate test graphs
    print("Creating performance graphs...")
    visualizer = PerformanceVisualizer()
    times = [datetime.now()]
    powers = [750]
    voltages = [48.5]
    
    graphs = {
        'power_graph': visualizer.create_power_graph(times, powers, 709),
        'voltage_graph': visualizer.create_voltage_graph(times, voltages, 51),
        'dashboard': visualizer.create_dashboard(test_data)
    }
    
    print("[OK] Graphs generated")
    print()
    
    # Send test alert
    print("Sending test power alert email...")
    print("This may take a few seconds...")
    print()
    
    success = sender.send_alert_email('power', test_data, graphs)
    
    if success:
        print("=" * 70)
        print("[SUCCESS] Test alert sent successfully!")
        print("=" * 70)
        print()
        print("Check these inboxes:")
        print("  1. nyakundi110@gmail.com")
        print("  2. carolinejosphat7@gmail.com")
        print()
        print("Subject: 🚨 Solar System Alert - High Power Detected")
        print()
        print("The email includes:")
        print("  - Alert details (Power: 750W)")
        print("  - System metrics (Voltage: 48.5V)")
        print("  - Performance graphs (24-hour trends)")
        print("  - System dashboard")
        print()
    else:
        print("=" * 70)
        print("[FAILED] Could not send test alert")
        print("=" * 70)
        print()
        print("Check the logs above for error details")
        sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
