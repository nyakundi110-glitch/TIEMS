"""
Configuration Loader for GrowattAlert
Loads configuration from environment variables with fallback to config.json
"""

import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def str_to_bool(value: str) -> bool:
    """Convert string to boolean"""
    return value.lower() in ('true', '1', 'yes', 'on')


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables first, 
    then fall back to config.json
    
    Returns:
        Dictionary containing all configuration settings
    """
    config = {
        'growatt': {},
        'email': {},
        'monitoring': {},
        'whatsapp': {},
        'logging': {}
    }
    
    # Try to load from config.json first as base configuration
    try:
        with open('config.json', 'r') as f:
            json_config = json.load(f)
            # Merge JSON config as base
            for key in config.keys():
                if key in json_config:
                    config[key] = json_config[key]
            logger.info("Loaded base configuration from config.json")
    except FileNotFoundError:
        logger.info("No config.json found, using environment variables only")
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON in config.json: {e}. Using environment variables only")
    
    # Override with environment variables (higher priority)
    # Growatt API Settings
    if os.getenv('GROWATT_USERNAME'):
        config['growatt']['username'] = os.getenv('GROWATT_USERNAME')
    if os.getenv('GROWATT_PASSWORD'):
        config['growatt']['password'] = os.getenv('GROWATT_PASSWORD')
    if os.getenv('GROWATT_API_TOKEN'):
        config['growatt']['api_token'] = os.getenv('GROWATT_API_TOKEN')
    if os.getenv('GROWATT_PLANT_ID'):
        config['growatt']['plant_id'] = os.getenv('GROWATT_PLANT_ID')
    if os.getenv('GROWATT_DEVICE_SN'):
        config['growatt']['device_sn'] = os.getenv('GROWATT_DEVICE_SN')
    if os.getenv('GROWATT_USE_API'):
        config['growatt']['use_api'] = str_to_bool(os.getenv('GROWATT_USE_API'))
    
    # Email Settings
    if os.getenv('SMTP_SERVER'):
        config['email']['smtp_server'] = os.getenv('SMTP_SERVER')
    if os.getenv('SMTP_PORT'):
        config['email']['smtp_port'] = int(os.getenv('SMTP_PORT'))
    if os.getenv('SENDER_EMAIL'):
        config['email']['sender_email'] = os.getenv('SENDER_EMAIL')
    if os.getenv('SENDER_PASSWORD'):
        config['email']['sender_password'] = os.getenv('SENDER_PASSWORD')
    if os.getenv('RECIPIENT_EMAILS'):
        # Parse comma-separated emails
        emails = [email.strip() for email in os.getenv('RECIPIENT_EMAILS').split(',')]
        config['email']['recipient_emails'] = emails
    if os.getenv('ENABLE_INSTANT_ALERTS'):
        config['email']['enable_instant_alerts'] = str_to_bool(os.getenv('ENABLE_INSTANT_ALERTS'))
    if os.getenv('ENABLE_DAILY_REPORTS'):
        config['email']['enable_daily_reports'] = str_to_bool(os.getenv('ENABLE_DAILY_REPORTS'))
    if os.getenv('DAILY_REPORT_TIME'):
        config['email']['daily_report_time'] = os.getenv('DAILY_REPORT_TIME')
    
    # Monitoring Settings
    if os.getenv('POWER_THRESHOLD'):
        config['monitoring']['power_threshold'] = float(os.getenv('POWER_THRESHOLD'))
    if os.getenv('VOLTAGE_THRESHOLD'):
        config['monitoring']['voltage_threshold'] = float(os.getenv('VOLTAGE_THRESHOLD'))
    if os.getenv('CHECK_INTERVAL_MINUTES'):
        config['monitoring']['check_interval_minutes'] = int(os.getenv('CHECK_INTERVAL_MINUTES'))
    if os.getenv('POWER_DURATION_HOURS'):
        config['monitoring']['power_duration_hours'] = float(os.getenv('POWER_DURATION_HOURS'))
    if os.getenv('VOLTAGE_ALERT_INTERVAL_HOURS'):
        config['monitoring']['voltage_alert_interval_hours'] = float(os.getenv('VOLTAGE_ALERT_INTERVAL_HOURS'))
    
    # WhatsApp Settings
    if os.getenv('WHATSAPP_GROUP_NAME'):
        config['whatsapp']['group_name'] = os.getenv('WHATSAPP_GROUP_NAME')
    if os.getenv('WHATSAPP_PHONE_NUMBER'):
        config['whatsapp']['phone_number'] = os.getenv('WHATSAPP_PHONE_NUMBER')
    
    # Logging Settings
    config['logging']['level'] = os.getenv('LOG_LEVEL', config.get('logging', {}).get('level', 'INFO'))
    config['logging']['file'] = os.getenv('LOG_FILE', config.get('logging', {}).get('file', 'solar_monitor.log'))
    
    # Validate required fields
    required_fields = [
        ('growatt', 'username'),
        ('growatt', 'password'),
        ('growatt', 'api_token'),
        ('growatt', 'plant_id'),
        ('growatt', 'device_sn'),
        ('email', 'smtp_server'),
        ('email', 'smtp_port'),
        ('email', 'sender_email'),
        ('email', 'sender_password'),
        ('email', 'recipient_emails'),
    ]
    
    missing_fields = []
    for section, field in required_fields:
        if section not in config or field not in config[section] or not config[section][field]:
            missing_fields.append(f"{section}.{field}")
    
    if missing_fields:
        error_msg = f"Missing required configuration fields: {', '.join(missing_fields)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("Configuration loaded successfully")
    logger.info(f"Email alerts enabled: {config['email'].get('enable_instant_alerts', True)}")
    logger.info(f"Daily reports enabled: {config['email'].get('enable_daily_reports', True)}")
    
    return config


if __name__ == "__main__":
    # Test configuration loading
    logging.basicConfig(level=logging.INFO)
    
    try:
        config = load_config()
        print("\n[OK] Configuration loaded successfully!")
        print(f"\nGrowatt Account: {config['growatt']['username']}")
        print(f"Email Sender: {config['email']['sender_email']}")
        print(f"Recipients: {', '.join(config['email']['recipient_emails'])}")
        print(f"Power Threshold: {config['monitoring']['power_threshold']}W")
        print(f"Voltage Threshold: {config['monitoring']['voltage_threshold']}V")
    except Exception as e:
        print(f"\n[ERROR] Configuration error: {e}")
