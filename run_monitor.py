#!/usr/bin/env python3
"""
Scheduled monitoring task for PythonAnywhere
Runs every 15 minutes to check solar system and send alerts

Usage:
  Configure as scheduled task in PythonAnywhere with:
  /usr/bin/python3.10 /home/YOUR_USERNAME/GrowattAlert/run_monitor.py
"""

import sys
import os
from datetime import datetime

# Add project directory to path - UPDATE THIS PATH!
PROJECT_PATH = '/home/YOUR_USERNAME/GrowattAlert'
sys.path.insert(0, PROJECT_PATH)
os.chdir(PROJECT_PATH)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print(f"[{datetime.now()}] Environment loaded from .env")
except ImportError:
    print(f"[{datetime.now()}] Warning: python-dotenv not installed, using system environment")
except Exception as e:
    print(f"[{datetime.now()}] Warning: Could not load .env: {e}")

# Import application components
try:
    from main import SolarMonitoringApp
    print(f"[{datetime.now()}] Starting monitoring check...")
    
    # Create app instance
    app = SolarMonitoringApp()
    
    # Run single monitoring check
    app.monitor_system()
    
    print(f"[{datetime.now()}] ✓ Monitoring check completed successfully")
    
except Exception as e:
    print(f"[{datetime.now()}] ✗ Error during monitoring: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
